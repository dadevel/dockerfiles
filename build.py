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


CACHE_DIR = Path('~/.cache/buildx').expanduser()
DEFAULT_PLATFORM = 'linux/amd64,linux/arm64/v8,linux/arm/v7'
DEFAULT_REF_MATCHER = '^refs/tags/v([0-9.]+)$'
REGISTRY = 'docker.io'
USERNAME = 'dadevel'
REPO_URL = 'https://github.com/dadevel/dockerfiles'


GitInfo = collections.namedtuple('GitInfo', ['source_url', 'latest_ref', 'latest_version', 'latest_commit', 'current_commit'])
MetaInfo = collections.namedtuple('MetaInfo', ['ref_matcher', 'version_adapter_target', 'version_adapter_replacement', 'platform'])
Image = collections.namedtuple('Image', ['path', 'registry', 'user', 'repo_url'])
RegistryCredentials = collections.namedtuple('RegistryCredentials', ['name', 'user', 'token'])


def main():
    running_in_ci = os.environ.get('CI')
    try:
        credentials = RegistryCredentials(REGISTRY, USERNAME, os.environ.get('REGISTRY_TOKEN'))
        if running_in_ci:
            login_registry(credentials)
            setup_git()
        setup_buildx()
        images = (Image(Path(item), credentials.name, credentials.user, REPO_URL) for item in sys.argv[1:])
        for image in images:
            process(image)
    finally:
        if running_in_ci:
            logout_registry(credentials)


def login_registry(creds):
    if not creds.token:
        raise RuntimeError('registry token missing')
    run('docker', 'login', creds.name, '--username', creds.user, '--password-stdin', stdin=creds.token)


def logout_registry(creds):
    run('docker', 'logout', creds.name)


def setup_git():
    run('git', 'config', 'user.name', 'GitHub Actions')
    run('git', 'config', 'user.email', 'actions@github.com')


def setup_buildx():
    docker('run', '--rm', '--privileged', 'multiarch/qemu-user-static:latest', '--reset', '--persistent', 'yes')
    try:
        docker('buildx', 'inspect', 'multiarch')
    except RuntimeError:
        docker('buildx', 'create', '--name', 'multiarch', '--use')
        docker('buildx', 'inspect', '--bootstrap', 'multiarch')


def process(image):
    meta_info = parse_meta_file(image.path/'meta.env')
    has_source = image.path.joinpath('src').is_dir()
    git_info = GitInfo(None, None, None, None, None)
    if has_source:
        git_info = fetch(image, meta_info)
        print(f'current commit {git_info.current_commit}, latest commit {git_info.latest_commit}, latest reference {git_info.latest_ref}, latest version {git_info.latest_version}')
    if has_source:
        checkout(image, git_info)
    build(image, git_info, meta_info.platform)
    if has_source:
        bump(image, git_info)


def fetch(image, meta_info):
    # update source
    run('git', 'submodule', 'update', '--init', '--recursive', image.path/'src')
    run('git', '-C', image.path/'src', 'fetch', '--tags')
    # find newest version
    latest_ref, latest_version = find_lastest_reference(image, meta_info.ref_matcher)
    # substitute in version if needed
    latest_version = adapt_version(
        latest_version,
        meta_info.version_adapter_target,
        meta_info.version_adapter_replacement,
    )
    return GitInfo(
        run('git', 'config', f'submodule.{image.path}/src.url', capture=True),
        latest_ref,
        latest_version,
        run('git', '-C', image.path/'src', 'rev-list', '--max-count=1', latest_ref, capture=True),
        run('git', '-C', image.path/'src', 'rev-parse', 'HEAD', capture=True),
    )


def parse_meta_file(path):
    try:
        values = load_envfile(path)
    except FileNotFoundError:
        return MetaInfo(None, None, None, DEFAULT_PLATFORM)
    return MetaInfo(
        re.compile(values.get('ref_matcher', DEFAULT_REF_MATCHER)),
        re.compile(values['version_adapter_target']) if 'version_adapter_target' in values else None,
        values.get('version_adapter_replacement'),
        values.get('platform', DEFAULT_PLATFORM),
    )


def find_lastest_reference(image, regex):
    if not regex:
        return None
    lines = run('git', '-C', image.path/'src', 'show-ref', capture=True).splitlines()
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
    run('git', '-C', image.path/'src', 'checkout', '--quiet', git_info.latest_ref)


def build(image, git_info, platform):
    tags = []
    for tag in generate_tags(git_info.latest_version):
        tags.extend(('--tag', f'{image.registry}/{image.user}/{image.path.name}:{tag}'))
    labels = []
    for label in generate_labels(image, git_info):
        labels.extend(('--label', f'org.opencontainers.image.{label}'))
    docker(
        'buildx', 'build',
        '--cache-from', f'type=local,src={CACHE_DIR}',
        '--cache-to', f'type=local,dest={CACHE_DIR}',
        '--platform', platform,
        *tags,
        *labels,
        '--push', image.path
    )


def generate_tags(version):
    yield 'latest'
    if version:
        yield from itertools.accumulate(version.split('.'), lambda a, b: f'{a}.{b}' if a else b)


def generate_labels(image, git_info):
    build_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    yield f'title={image.path.name}'
    yield f'authors={image.user}'
    yield f'url={image.repo_url}'
    yield f'created={build_date}'
    if git_info.latest_version:
        yield f'version={git_info.latest_version}'
    if git_info.latest_commit:
        yield f'revision={git_info.latest_commit}'
    if git_info.source_url:
        yield f'source={git_info.source_url}'


def bump(image, git_info):
    if git_info.latest_commit != git_info.current_commit:
        run('git', 'add', image.path/'src')
        target = f'v{git_info.latest_version}' if git_info.latest_version else f'{git_info.latest_commit[:7]}'
        run('git', 'commit', '--message', f'{image.path.name}: bump version to {target}')
        run('git', 'push')


def docker(*args):
    if sudo_needed():
        run('sudo', 'DOCKER_BUILDKIT=1', 'DOCKER_CLI_EXPERIMENTAL=enabled', 'docker', *args)
    else:
        run('env', 'DOCKER_BUILDKIT=1', 'DOCKER_CLI_EXPERIMENTAL=enabled', 'docker', *args)


def sudo_needed():
    return 'docker' not in get_groups()


def get_groups():
    return [grp.getgrgid(gid).gr_name for gid in os.getgroups()]


def load_envfile(path):
    with open(path) as file:
        lines = [line.split('=', maxsplit=1) for line in file if line.strip() and not line.startswith('#')]
        return {key: value.rstrip() for key, value in lines}


def run(*args, stdin=None, capture=False):
    args = [str(item) for item in args if item is not None]
    cmdline = ' '.join(args)
    print('>', cmdline)
    process = subprocess.run(args, input=stdin, text=True, check=False, capture_output=capture)
    if process.returncode != 0:
        raise RuntimeError(f'subprocess failed with exit code {process.returncode}: {cmdline}')
    if capture:
        return process.stdout.strip()


if __name__ == '__main__':
    main()

