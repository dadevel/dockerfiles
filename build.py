#!/usr/bin/env python3
from contextlib import contextmanager
from datetime import datetime
from distutils.version import LooseVersion
from pathlib import Path

import collections
import grp
import itertools
import shlex
import subprocess
import os
import re
import sys


GitInfo = collections.namedtuple('GitInfo', ['source_url', 'latest_ref', 'latest_version', 'latest_commit', 'current_commit'])
Image = collections.namedtuple('Image', ['path', 'registry', 'user', 'repo_url'])
RegistryCredentials = collections.namedtuple('RegistryCredentials', ['name', 'user', 'token'])


BUILD_ORDER = [
    # base
    'alpine', 'distroless', 'python',
    # builder
    'c-builder', 'go-builder',
    # c-based
    'chrony', 'dnsmasq', 'unbound',
    # go-based
    'cadvisor', 'traefik', 'watchtower',
    # other
    'prometheus-smart-collector',
]


def main():
    repo_url = os.environ.get('REPO_URL', 'https://github.com/dadevel/dockerfiles')
    architectures = os.environ.get('ARCHITECTURES', 'linux/amd64,linux/arm64,linux/arm/v7')
    cache = Path(os.environ.get('CACHE', '~/.cache/buildx')).expanduser()
    running_in_ci = os.environ.get('CI')
    if running_in_ci and os.environ.get('GITHUB_EVENT_NAME') == 'push':
        print('running on push')
        first = os.environ.get('COMMIT_BEFORE')
        last = os.environ.get('COMMIT_NOW')
        images = changes(first, last)
    else:
        print('running on schedule')
        images = sys.argv[1:]
    try:
        credentials = registry_credentials_from_env()
        if running_in_ci:
            login_registry(credentials)
        setup_buildx()
        for item in images:
            image = Image(Path(item), credentials.name, credentials.user, repo_url)
            process(image, cache, architectures)
    finally:
        if running_in_ci:
            logout_registry(credentials)


def into_build_order(it):
    return list(sorted(it, key=lambda item: BUILD_ORDER.index(item)))


def registry_credentials_from_env():
    try:
        return RegistryCredentials('docker.io', 'dadevel', os.environ.get('REGISTRY_TOKEN'))
    except KeyError as e:
        raise RuntimeError('environment variable {e} undefined') from e


def login_registry(creds):
    assert creds.token, 'registry token missing or empty'
    run('docker', 'login', creds.name, '--username', creds.user, '--password-stdin', stdin=creds.token)


def logout_registry(creds):
    run('docker', 'logout', creds.name)


def setup_buildx():
    docker('run', '--rm', '--privileged', 'multiarch/qemu-user-static:latest', '--reset', '--persistent', 'yes')
    try:
        docker('buildx', 'inspect', 'multiarch')
    except SubprocessError:
        docker('buildx', 'create', '--name', 'multiarch', '--use')
        docker('buildx', 'inspect', '--bootstrap', 'multiarch')


def changes(first_commit, last_commit):
    try:
        paths = [Path(line) for line in run('git', 'diff', '--name-only', first_commit, last_commit).splitlines()]
        result = {path.parent for path in paths if path.parent.joinpath('Dockerfile').is_file()}
        result = into_build_order(result)
    except SubprocessError:
        result = BUILD_ORDER
    print(f'rebuilding images {", ".join(str(x) for x in result)}')
    return result


def process(image, cache_dir, architectures):
    has_source = image.path.joinpath('src').is_dir()
    git_info = fetch(image) if has_source else GitInfo(None, None, None, None, None)
    print(f'current commit {git_info.current_commit}, latest commit {git_info.latest_commit}, latest reference {git_info.latest_ref}, latest version {git_info.latest_version}')
    if has_source:
        checkout(image, git_info)
    build(image, git_info, cache_dir, architectures)
    if has_source:
        bump(image, git_info)


def fetch(image):
    # update source
    run('git', 'submodule', 'update', '--init', '--recursive', image.path/'src')
    ref_matcher, version_adapter_target, version_adapter_replacement = parse_meta_file(image.path/'meta.env')
    # find newest version
    latest_ref, latest_version = find_lastest_reference(image, ref_matcher)
    latest_version = adapt_version(latest_version, version_adapter_target, version_adapter_replacement)
    return GitInfo(
        run('git', 'config', f'submodule.{image.path}/src.url'),
        latest_ref,
        latest_version,
        latest_commit=run('git', '-C', image.path/'src', 'rev-list', '--max-count=1', latest_ref),
        current_commit=run('git', '-C', image.path/'src', 'rev-parse', 'HEAD')
    )


def parse_meta_file(path):
    variables = load_envfile(path)
    try:
        matcher = re.compile(variables['ref_matcher'])
    except KeyError as e:
        raise RuntimeError('ref_matcher not defined in meta.env') from e
    try:
        adapter_target = re.compile(variables['version_adapter_target'])
        adapter_replacement = variables['version_adapter_replacement']
    except KeyError:
        adapter_target = None
        adapter_replacement = None
    return matcher, adapter_target, adapter_replacement


def find_lastest_reference(image, regex):
    lines = run('git', '-C', image.path/'src', 'show-ref').splitlines()
    refs = [line.split(' ')[1] for line in lines]
    matches = [(ref, match) for ref in refs if (match := regex.match(ref))]
    if len(matches) == 1:
        return matches[-1][0], None
    versions = [(ref, match.group(1)) for ref, match in matches]
    sorted_versions = sorted(versions, key=lambda pair: LooseVersion(pair[1]))
    return sorted_versions[-1]


def adapt_version(version, adapter_target, adapter_replacement):
    if adapter_target is None or adapter_replacement is None:
        return version
    return adapter_target.sub(adapter_replacement, version)


def checkout(image, git_info):
    run('git', '-C', image.path/'src', 'fetch', 'origin', git_info.latest_ref)
    run('git', '-C', image.path/'src', 'checkout', git_info.latest_ref)


def build(image, git_info, cache_dir, platform):
    build_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    tag_args = [
        ('--tag', f'{image.registry}/{image.user}/{image.path.name}:{tag}')
        for tag in generate_tags(git_info.latest_version)
    ]
    docker(
        'buildx', 'build',
        '--cache-from', f'type=local,src={cache_dir}',
        '--cache-to', f'type=local,dest={cache_dir}',
        '--platform', platform,
        *tag_args,
        '--label', f'org.opencontainers.image.title={image.path.name}',
        '--label', f'org.opencontainers.image.authors={image.user}',
        '--label', f'org.opencontainers.image.url={image.repo_url}',
        '--label', f'org.opencontainers.image.created={build_date}',
        ('--label', f'org.opencontainers.image.version={git_info.latest_version}') if git_info.latest_version else None,
        ('--label', f'org.opencontainers.image.revision={git_info.latest_commit}') if git_info.latest_commit else None,
        ('--label', f'org.opencontainers.image.source={git_info.source_url}') if git_info.source_url else None,
        '--push', image.path
    )


def generate_tags(version):
    yield 'latest'
    if version:
        yield from itertools.accumulate(version.split('.'), lambda a, b: f'{a}.{b}' if a else b)


def bump(image, git_info):
    if git_info.latest_commit != git_info.current_commit:
        run('git', 'add', image.path/'src')
        run('git', 'commit', '--message', f'{image.path.name}: bump version to v{git_info.latest_version}' if git_info.latest_version else f'{image.path.name}: bump version to {git_info.latest_commit[:7]}')
        run('git', 'push')


def docker(*args):
    if sudo_needed():
        return system('sudo', 'DOCKER_BUILDKIT=1', 'DOCKER_CLI_EXPERIMENTAL=enabled', 'docker', *args)
    else:
        return system('env', 'DOCKER_BUILDKIT=1', 'DOCKER_CLI_EXPERIMENTAL=enabled', 'docker', *args)


def sudo_needed():
    return 'docker' not in get_groups()


def get_groups():
    return [grp.getgrgid(gid).gr_name for gid in os.getgroups()]


def load_envfile(path):
    with open(path) as file:
        lines = [line.split('=', maxsplit=1) for line in file]
        return {key: value.rstrip() for key, value in lines}


def run(*args, stdin=None, text=True, **kwargs):
    command = filter_command(args)
    print(' '.join(command))
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=text, **kwargs)
    out, err = process.communicate(stdin)
    rc = process.wait()
    if rc != 0:
        raise SubprocessError(' '.join(command), err)
    return out.strip()


def system(*args):
    command = ' '.join(shlex.quote(item) for item in filter_command(args))
    print(command)
    err = os.system(command)
    if err != 0:
        raise SubprocessError(command)


class SubprocessError(Exception):
    def __init__(self, command, error=None):
        self.command = command
        self.error = error.strip() if error else None
        super().__init__(f'subprocess failed: {self.error}' if self.error else 'subprocess failed')


def filter_command(args):
    command = []
    for item in args:
        if isinstance(item, tuple):
            command.extend(str(x) for x in item)
        elif item is not None:
            command.append(str(item))
    return command


if __name__ == '__main__':
    main()

