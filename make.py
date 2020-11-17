#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import datetime
from distutils.version import LooseVersion
from pathlib import Path

import collections
import grp
import itertools
import json
import subprocess
import os
import re
import sys
import time


def main(args):
    main_parser = ArgumentParser()
    subparsers = main_parser.add_subparsers(dest='command', required=True)

    parser = subparsers.add_parser('publish')
    parser.add_argument('--cache', type=lambda x: Path(x).expanduser(), default=Path.cwd()/'.cache', metavar='DIRECTORY')
    parser.add_argument('images', nargs='*', metavar='IMAGE')

    parser = subparsers.add_parser('test')
    parser.add_argument('--cache', type=lambda x: Path(x).expanduser(), default=Path.cwd()/'.cache', metavar='DIRECTORY')
    parser.add_argument('images', nargs='*', metavar='IMAGE')

    parser = subparsers.add_parser('generate')
    subsubparsers = parser.add_subparsers(dest='subcommand', required=True)
    parser = subsubparsers.add_parser('ci')

    opts = main_parser.parse_args(args)
    opts.images = getattr(opts, 'images', [])
    commands = dict(
        test=do_test,
        publish=do_publish,
        generate_ci=do_generate_ci,
    )
    command = commands[f'{opts.command}_{opts.subcommand}' if hasattr(opts, 'subcommand') else opts.command]
    command(opts)


def do_test(opts):
    index = Index().load()
    if opts.images:
        index = index.apply_image_whitelist(opts.images)
    index = index.gather_image_dependencies()

    setup_buildx()
    for image in index.images:
        image.start_build_process(index.registries, opts.cache)


def do_publish(opts):
    index = Index().load()
    index = index.resolve_registry_tokens()
    if opts.images:
        index = index.apply_image_whitelist(opts.images)
    index = index.gather_image_dependencies()

    try:
        for registry in index.registries:
            registry.login()
        setup_buildx()
        for image in index.images:
            image.start_build_process(index.registries, opts.cache)
    finally:
        for registry in index.registries:
            registry.logout()


def do_generate_ci(opts):
    index = Index().load()
    if opts.images:
        index = index.apply_image_whitelist(opts.images)
    index = index.gather_image_dependencies()

    data = generate_actions_config(index)
    try:
        import yaml
        text = yaml.safe_dump(data, indent=2, sort_keys=False)
    except ImportError:
        text = json.dumps(data, indent=2, sort_keys=False)
    print(text)


def generate_actions_config(index):
    return {
        'name': 'CI',
        "on": {
          'schedule': [
              {'cron': '0 3 * * *'},
          ],
        },
        'jobs': {image.name: generate_job(image, index.registries) for image in index.images},
    }


def generate_job(image, registries):
    return {
        'runs-on': 'ubuntu-20.04',
        'needs': image.dependencies,
        'steps': [
            {
                'name': 'Checkout',
                'uses': 'actions/checkout@v2',
                'with': {
                    'fetch-depth': 0,
                }
            },
            {
                'name': 'Build, Test & Push',
                'run': f'./make.py publish {image.name}',
                'env': {
                    registry.key: '${{ secrets.' + registry.key + ' }}'
                    for registry in registries
                },
            },
        ],
    }

# classes

class Repository:
    def __init__(self, path, source=None, version=None, correction=None, latest_ref=None, latest_version=None, latest_commit=None, current_commit=None):
        self.path = path
        self.source = source
        self.version = re.compile(version) if isinstance(version, str) else version
        self.correction = correction
        self.latest_ref = latest_ref
        self.latest_version = latest_version
        self.latest_commit = latest_commit
        self.current_commit = current_commit

    def update(self, **kwargs):
        values = dict(self.__dict__, **kwargs)
        return Repository(**values)

    def clone(self):
        if self.path.joinpath('.git').exists():
            git('-C', self.path, 'reset', 'origin/HEAD')
            git('-C', self.path, 'pull', 'origin', 'HEAD', '--rebase')
        else:
            git('clone', self.source, self.path)
        latest_ref, latest_version = self._find_lastest_reference()
        latest_version = self._correct_version(latest_version, self.correction)
        return self.update(
            latest_ref=latest_ref,
            latest_version=latest_version,
            latest_commit=git('-C', self.path, 'rev-list', '--max-count=1', latest_ref, capture=True),
            current_commit=git('-C', self.path, 'rev-parse', 'HEAD', capture=True),
        )

    def checkout(self):
        git('-C', self.path, 'checkout', '--quiet', self.latest_ref)
        return self

    def _find_lastest_reference(self):
        lines = git('-C', self.path, 'show-ref', capture=True).splitlines()
        refs = []
        for line in lines:
            words = line.split(' ', maxsplit=1)
            if len(words) != 2:
                raise RuntimeError('could not parse output from git show-ref')
            _hash, ref = words
            refs.append(ref)

        matches = list()
        for ref in refs:
            assert self.version
            match = self.version.match(ref)
            if match:
                matches.append((ref, match))

        versions = [(ref, match.group(1)) for ref, match in matches]
        sorted_versions = sorted(versions, key=lambda pair: LooseVersion(pair[1]))
        latest_ref, latest_version = sorted_versions[-1]
        return latest_ref, latest_version

    @staticmethod
    def _correct_version(version, correction):
        return version.replace(correction['search'], correction['replace'])


class Image:
    dependency_extraction_regex = re.compile(r'from\s+(?:--platform=[^\s]+\s+)?(?P<image>[^\s:]+)(?::(?P<tag>[^\s]+))?(?:\s+as\s+[^\s]+)?')

    def __init__(self, name, path=None, repository=None, platforms=None, dependencies=None, labels=None, build_date=None):
        self.name = name
        self.path = path
        self.repository = repository
        self.platforms = platforms
        self.dependencies = dependencies if dependencies else list()
        self.labels = labels if labels else list()
        self.build_date = build_date

    def update(self, **kwargs):
        values = dict(self.__dict__, **kwargs)
        return Image(**values)

    def gather_dependencies(self):
        dependencies = list(sorted(set(self._extract_dependencies(self.path/'Dockerfile'))))
        # TODO: don't hardcode prefix
        prefix = 'dadevel/'
        return self.update(
            dependencies=[
                image_name[len(prefix):]
                for image_name in dependencies
                if image_name.startswith(prefix)
            ]
        )

    def _extract_dependencies(self, dockerfile):
        # TODO: don't forget COPY --from=image
        with open(dockerfile) as file:
            for line in file:
                match = self.dependency_extraction_regex.match(line.strip().lower())
                if match:
                    yield match.group('image')

    def start_build_process(self, registries, cache):
        image = self
        if image.repository.source:
            image = image.update(repository=image.repository.clone().checkout())
        image_name = image._build_test(cache)
        image._run_test(image_name)
        image = image._build_release(registries, cache)
        return image

    def _build_test(self, cache):
        # TODO: don't hardcode registry
        image_name = f'ghcr.io/dadevel/{self.name}:testing'
        docker(
            'buildx', 'build',
            '--cache-from', f'type=local,src={cache}',
            '--cache-to', f'type=local,dest={cache}',
            '--platform', ','.join(self.platforms),
            '--tag', image_name,
            '--push', self.path,
        )
        return image_name

    def _run_test(self, image_name):
        docker('pull', image_name)
        has_healthcheck = bool(json.loads(docker('image', 'inspect', image_name, '--format', '{{json .Config.Healthcheck}}', capture=True)))
        if has_healthcheck:
            self._test_healthcheck(image_name)
        else:
            self._test_startup(image_name)

    def _test_healthcheck(self, image_name):
        cid = docker(
            'run', '--detach', '--rm', '--tty',
            '--health-interval', '1s',
            '--health-retries', '60',
            '--health-start-period', '1s',
            '--health-timeout', '1s',
            image_name, capture=True
        )
        for _ in range(60):
            time.sleep(1)
            state = json.loads(docker('container', 'inspect', cid, '--format', '{{json .State}}', capture=True))
            status = state['Status']
            health = state['Health'].get('Status')
            if status in ('dead', 'exited'):
                raise RuntimeError(f'image {self.name} failed to start up')
            if health == 'healthy':
                return
        raise RuntimeError(f'image {self.name} failed the health check')

    def _test_startup(self, image_name):
        cid = docker('run', '--detach', '--rm', '--tty', image_name, capture=True)
        for _ in range(60):
            time.sleep(1)
            status = docker('container', 'inspect', cid, '--format', '{{.State.Status}}', capture=True)
            if status in ('dead', 'exited'):
                raise RuntimeError(f'image {self.name} failed to start up')
            if status == 'running':
                return
        raise RuntimeError(f'image {self.name} did not start in time')

    def _build_release(self, registries, cache):
        image = self

        tags = []
        for tag in self._generate_tags(self.repository.latest_version):
            for registry in registries:
                tags.extend(('--tag', f'{registry.name}/{registry.user}/{self.name}:{tag}'))

        image = image.update(build_date=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'))
        image = image._render_labels()
        labels = []
        for key, value in image.labels.items():
            labels.extend(('--label', f'{key}={value}'))

        docker(
            'buildx', 'build',
            '--cache-from', f'type=local,src={cache}',
            '--cache-to', f'type=local,dest={cache}',
            '--platform', ','.join(image.platforms),
            *tags,
            *labels,
            '--push', image.path,
        )
        return image

    @staticmethod
    def _generate_tags(version):
        yield 'latest'
        if version:
            yield from itertools.accumulate(version.split('.'), lambda a, b: f'{a}.{b}' if a else b)

    def _render_labels(self):
        temp = self.update(
            repository=self.repository.update(
                latest_version=self.repository.latest_version if self.repository.latest_version else 'unknown',
                latest_commit=self.repository.latest_commit if self.repository.latest_commit else 'unknown',
                source=self.repository.source if self.repository.source else 'unknown',
            )
        )
        labels = {
            key: value.format(image=temp)
            for key, value in self.labels.items()
        }
        return self.update(labels=labels)


class Registry:
    def __init__(self, name, user, token=None):
        self.name = name
        self.user = user
        self.token = token

    @property
    def key(self):
        return f'{self.name.replace(".", "").upper()}_TOKEN'

    def update(self, **kwargs):
        values = dict(self.__dict__, **kwargs)
        return Registry(**values)

    def resolve_token(self):
        return self.update(token=os.environ[self.key])

    def login(self):
        docker('login', self.name, '--username', self.user, '--password-stdin', stdin=self.token)
        return self

    def logout(self):
        docker('logout', self.name, check=False)
        return self


class Index:
    def __init__(self, path=None, images=None, registries=None):
        self.path = path if path else Path.cwd()/'index.json'
        self.images = images if images else list()
        self.registries = registries if registries else list()

    def update(self, **kwargs):
        values = dict(self.__dict__, **kwargs)
        return Index(**values)

    def load(self):
        with open(self.path) as file:
            data = json.load(file)

        repo_keys = ('source', 'version', 'correction')
        default = Image(
            None,
            repository=Repository(
                None,
                **{key: value for key, value in data['defaults'].items() if key in repo_keys}
            ),
            **{key: value for key, value in data['defaults'].items() if key not in repo_keys}
        )

        images = [
            default.update(
                repository=default.repository.update(
                    path=Path.cwd()/image['name']/'src',
                    **{key: value for key, value in image.items() if key in repo_keys}
                ),
                path=Path.cwd()/image['name'],
                **{key: value for key, value in image.items() if key not in repo_keys}
            )
            for image in data['images']
        ]

        images = [image.gather_dependencies() for image in images]
        registries = [Registry(**item) for item in data['registries']]
        return self.update(images=images, registries=registries)

    def apply_image_whitelist(self, image_names):
        table = {image.name: image for image in self.images}
        return self.update(images=[table[name] for name in image_names])

    def gather_image_dependencies(self):
        return self.update(images=[image.gather_dependencies() for image in self.images])

    def resolve_registry_tokens(self):
        return self.update(registries=[registry.resolve_token() for registry in self.registries])

# utils

def setup_buildx():
    docker('run', '--rm', '--privileged', 'multiarch/qemu-user-static:latest', '--reset', '--persistent', 'yes')
    try:
        docker('buildx', 'inspect', 'multiarch')
    except RuntimeError:
        docker('buildx', 'create', '--name', 'multiarch', '--use')
        docker('buildx', 'inspect', '--bootstrap', 'multiarch')


def docker(*args, **kwargs):
    sudo = () if 'docker' in user_groups() else ('sudo', '-E')
    return run(*sudo, 'docker', *args, env=dict(DOCKER_CLI_EXPERIMENTAL='enabled', BUILDX_NO_DEFAULT_LOAD='false'), **kwargs)


def git(*args, **kwargs):
    return run('git', *args, **kwargs)


def user_groups():
    return [grp.getgrgid(gid).gr_name for gid in os.getgroups()]


def run(*args, stdin=None, capture=False, check=True, env=None):
    args = [str(item) for item in args if item is not None]
    cmdline = ' '.join(args)
    print('>', cmdline, flush=True)
    environment = dict(os.environ, **env) if env else None
    process = subprocess.run(args, input=stdin, text=True, check=False, capture_output=capture, env=environment)
    if capture:
        print(process.stdout, end='', flush=True)
    if check and process.returncode != 0:
        message = f'{cmdline}: {process.stderr.strip()}' if process.stderr else cmdline
        raise RuntimeError(f'subprocess failed with exit code {process.returncode}: {message}')
    if capture:
        return process.stdout.strip()


if __name__ == '__main__':
    main(sys.argv[1:])

