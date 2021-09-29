#!/usr/bin/env python3
from __future__ import annotations
from argparse import ArgumentParser, Namespace
from datetime import datetime
from distutils.version import LooseVersion
from pathlib import Path
from typing import Any, Generator, Optional

import dataclasses
import grp
import itertools
import json
import os
import re
import subprocess

QEMU_IMAGE = 'docker.io/multiarch/qemu-user-static:latest'
BUILDER_NAME = 'multiarch'
FALLBACK_PLATFORM = 'linux/amd64'
DOCKERFILE_DEPENDENCY_PATTERNS = (
    re.compile(r'from\s+(?:--platform=[^\s]+\s+)?(?P<image>[^\s:]+)(?::(?P<tag>[^\s]+))?(?:\s+as\s+[^\s]+)?'),
    re.compile(r'copy\s+--from=(?P<image>[^\s:]+)(?::(?P<tag>[^\s]+))?\s+.*'),
)
WORKFLOW_PATH = '.github/workflows/ci.yaml'


@dataclasses.dataclass
class Registry:
    name: str
    user: Optional[str]
    password: Optional[str]

    @classmethod
    def from_env(cls):
        return cls(
            os.environ.get('REGISTRY_NAME', 'localhost'),
            os.environ.get('REGISTRY_USER'),
            os.environ.get('REGISTRY_PASS')
        )

    def __post_init__(self):
        self.can_authenticate = self.name and self.user and self.password

    def login(self):
        if self.can_authenticate:
            docker('login', self.name, '--username', self.user, '--password-stdin', stdin=self.password)

    def logout(self):
        if self.can_authenticate:
            docker('logout', self.name, check=False)


@dataclasses.dataclass
class Configuration:
    workdir: Path
    cache: Path
    registry: Registry
    defaults: dict[str, Any]

    @classmethod
    def from_dir(cls, path: Path):
        return cls(
            path,
            path/'.cache',
            Registry.from_env(),
            read_json(path/'default.json'),
        )

    def setup_cache(self):
        self.cache.mkdir(exist_ok=True)

    @staticmethod
    def setup_docker_buildx() -> None:
        docker('run', '--rm', '--privileged', QEMU_IMAGE, '--reset', '--persistent', 'yes')
        try:
            docker('buildx', 'inspect', BUILDER_NAME)
        except RuntimeError:
            docker('buildx', 'create', '--name', BUILDER_NAME, '--use')
            docker('buildx', 'inspect', '--bootstrap', BUILDER_NAME)


@dataclasses.dataclass
class BuildInfo:
    source: str
    version: re.Pattern
    correction: dict[str, str]
    platforms: list[str]
    labels: dict[str, str]

    @classmethod
    def from_file(cls, path: Path) -> BuildInfo:
        attrs = CONFIG.defaults.copy()
        if path.exists():
            override = read_json(path)
            labels = attrs['labels'].copy()
            labels.update(override.get('labels', dict()))
            attrs.update(override, labels=labels)
        return BuildInfo(
            attrs['source'],
            re.compile(attrs['version']),
            attrs['correction'],
            attrs['platforms'],
            attrs['labels'],
        )


@dataclasses.dataclass
class Repository:
    path: Path

    def clone(self, build_info: BuildInfo) -> VersionInfo:
        git_dir = self.path/'.git'
        if git_dir.is_dir():
            git('-C', self.path, 'reset', '--hard', 'origin/HEAD')
            git('-C', self.path, 'pull', 'origin', 'HEAD', '--rebase')
        else:
            git('clone', build_info.source, self.path)
        latest_ref, latest_version = self._find_lastest_ref(build_info.version)
        latest_version = self._correct_version(latest_version, build_info.correction)
        return VersionInfo(
            latest_ref,
            latest_version,
            git('-C', self.path, 'rev-list', '--max-count=1', latest_ref, capture=True),
            git('-C', self.path, 'rev-parse', 'HEAD', capture=True),
        )

    def checkout(self, version_info: VersionInfo) -> None:
        git('-C', self.path, 'checkout', '--quiet', version_info.latest_ref)

    def _find_lastest_ref(self, version_regex: re.Pattern) -> tuple[str, str]:
        lines = git('-C', self.path, 'show-ref', capture=True).splitlines()
        refs = []
        for line in lines:
            words = line.split(' ', maxsplit=1)
            if len(words) != 2:
                raise RuntimeError('could not parse output from git show-ref')
            _, ref = words
            refs.append(ref)

        matches = list()
        for ref in refs:
            match = version_regex.fullmatch(ref)
            if match:
                matches.append((ref, match))

        versions = [(ref, match.group(1)) for ref, match in matches]
        sorted_versions = sorted(versions, key=lambda pair: LooseVersion(pair[1]))
        latest_ref, latest_version = sorted_versions[-1]
        return latest_ref, latest_version

    @staticmethod
    def _correct_version(version: str, correction: dict[str, str]) -> str:
        return version.replace(correction['search'], correction['replace'])


@dataclasses.dataclass
class VersionInfo:
    latest_ref: str
    latest_version: str
    latest_commit: str
    current_commit: str

    @classmethod
    def empty(cls):
        return cls('', '', '', '')


@dataclasses.dataclass
class ContainerImage:
    path: Path
    build_info: BuildInfo
    repo: Repository

    @classmethod
    def from_file(cls, path: Path):
        return cls(path, BuildInfo.from_file(path/'build.json'), Repository(path/'src'))

    def __post_init__(self):
        self.name = '/'.join(item for item in (CONFIG.registry.name, CONFIG.registry.user, self.path.name) if item)

    def build(self):
        if self.build_info.source:
            version_info = self.repo.clone(self.build_info)
            self.repo.checkout(version_info)
        else:
            version_info = VersionInfo.empty()

        if self.path.joinpath('Dockerfile').exists():
            self._build_image(self.path/'Dockerfile', version_info, tag_postfix='')
        for dockerfile in self.path.glob('*.Dockerfile'):
            self._build_image(dockerfile, version_info,tag_postfix=dockerfile.with_suffix('').name)

    def _build_image(self, dockerfile: Path, version_info: VersionInfo, tag_postfix: str):
        tags = []
        for tag in self._generate_image_tags(version_info, tag_postfix):
            tags.extend(('--tag', f'{self.name}:{tag}'))

        labels = []
        for key, value in self._generate_image_labels(version_info).items():
            labels.extend(('--label', f'{key}={value}'))

        docker(
            'buildx', 'build',
            '--cache-from', f'type=local,src={CONFIG.cache}',
            '--cache-to', f'type=local,dest={CONFIG.cache}',
            '--platform', ','.join(self.build_info.platforms) if CONFIG.registry.can_authenticate else FALLBACK_PLATFORM,
            *tags,
            *labels,
            '--push' if CONFIG.registry.can_authenticate else '--load',
            '--file', dockerfile,
            self.path,
        )

    @staticmethod
    def _generate_image_tags(version_info: VersionInfo, postfix: str) -> Generator[str, None, None]:
        yield postfix if postfix else 'latest'
        if version_info.latest_version:
            yield from itertools.accumulate(
                version_info.latest_version.split('.'),
                lambda a, b: f'{a}.{b}-{postfix}' if postfix else f'{a}.{b}' if a else b,
            )

    def _generate_image_labels(self, version_info: VersionInfo):
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        labels = {
            key: value.format(image=self, build=self.build_info, version=version_info, timestamp=timestamp)
            for key, value in self.build_info.labels.items()
        }
        labels = {key: value for key, value in labels.items() if value}
        return labels


def main():
    entrypoint = ArgumentParser()
    entrypoint.add_argument('-w', '--workdir', type=Path, default=Path.cwd(), metavar='PATH')
    subparsers = entrypoint.add_subparsers(dest='command', required=True)
    parser = subparsers.add_parser('image')
    parser.add_argument('image', nargs='+', type=Path)
    parser = subparsers.add_parser('workflow')
    opts = entrypoint.parse_args()
    global CONFIG
    CONFIG = Configuration.from_dir(opts.workdir)
    commands = dict(
        image=build_images,
        workflow=write_workflow,
    )
    commands[opts.command](opts)


def build_images(opts: Namespace) -> None:
    CONFIG.setup_cache()
    CONFIG.setup_docker_buildx()
    CONFIG.registry.login()
    try:
        for path in opts.image:
            image = ContainerImage.from_file(path)
            image.build()
    finally:
        CONFIG.registry.logout()


@dataclasses.dataclass
class Job:
    dockerfile: Path
    build_info: BuildInfo

    @classmethod
    def from_file(cls, dockerfile: Path) -> Job:
        return cls(dockerfile, BuildInfo.from_file(dockerfile.parent/'build.json'))

    def __post_init__(self):
        self.dependencies = self._gather_dependencies()

    @property
    def name(self) -> str:
        return self.dockerfile.parent.name

    def _gather_dependencies(self) -> list[str]:
        prefix = f'{CONFIG.registry.name}/{CONFIG.registry.user}/'
        dependencies = list(sorted(set(self._extract_dependencies())))
        return [
            image_name[len(prefix):]
            for image_name in dependencies
            if image_name.startswith(prefix)
        ]

    def _extract_dependencies(self) -> Generator[str, None, None]:
        with open(self.dockerfile) as file:
            for line in file:
                image_name = self._match_dependency_pattern(line)
                if image_name:
                    yield image_name

    @staticmethod
    def _match_dependency_pattern(line: str) -> Optional[str]:
        for pattern in DOCKERFILE_DEPENDENCY_PATTERNS:
            match = pattern.fullmatch(line.strip().lower())
            if match:
                return match.group('image')
        return None

    def generate(self) -> dict[str, Any]:
        return {
            'runs-on': 'ubuntu-20.04',
            'needs': self.dependencies,
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
                    'run': f'./build.py image {self.name}',
                    'env': {
                        'REGISTRY_NAME': CONFIG.registry.name,
                        'REGISTRY_USER': CONFIG.registry.user,
                        'REGISTRY_PASS': '${{ secrets.GITHUB_TOKEN }}'
                    },
                },
            ],
        }


def write_workflow(opts: Namespace) -> None:
    import yaml
    jobs = [
        Job.from_file(path)
        for path in sorted(
            itertools.chain(
                opts.workdir.glob('*/Dockerfile'),
                opts.workdir.glob('*/*.Dockerfile'),
            )
        )
    ]
    data = {
        'name': 'CI',
        'on': {
            'push': {
                'branches': [
                    'main',
                ],
            },
            'schedule': [
                {'cron': '0 3 * * *'},
            ],
        },
        'jobs': {job.name: job.generate() for job in jobs},
    }
    text = yaml.safe_dump(data, indent=2, sort_keys=False)
    # remove quotes around `on` key
    text = text.replace("\n'on':\n", '\non:\n')
    CONFIG.workdir.joinpath(WORKFLOW_PATH).write_text(text)


def docker(*args: Any, **kwargs: Any) -> str:
    groups = {grp.getgrgid(gid).gr_name for gid in os.getgroups()}
    sudo = () if 'docker' in groups else ('sudo', '--preserve-env=DOCKER_CLI_EXPERIMENTAL,BUILDX_NO_DEFAULT_LOAD')
    envvars = dict(DOCKER_CLI_EXPERIMENTAL='enabled', BUILDX_NO_DEFAULT_LOAD='false')
    return run(*sudo, 'docker', *args, env=envvars, **kwargs)


def git(*args: Any, **kwargs: Any) -> str:
    return run('git', *args, **kwargs)


def run(*args: Any, stdin: str = None, capture: bool = False, check: bool = True, env: dict[str, Any] = None) -> str:
    args = tuple(str(item) for item in args if item is not None)
    cmdline = ' '.join(args)
    print('>', cmdline, flush=True)
    environment = dict(os.environ, **env) if env else None
    process = subprocess.run(args, input=stdin, text=True, check=False, capture_output=capture, env=environment)
    if check and process.returncode != 0:
        message = f'{cmdline}: {process.stderr.strip()}' if process.stderr else cmdline
        raise RuntimeError(f'subprocess failed with exit code {process.returncode}: {message}')
    return process.stdout.strip() if capture else ''


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


if __name__ == '__main__':
    main()
