#!/usr/bin/env python3
from __future__ import annotations
from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path
from typing import Any, Generator, Optional

import dataclasses
import grp
import itertools
import json
import os
import re
import subprocess

DOCKERFILE_DEPENDENCY_PATTERNS = (
    re.compile(r'from\s+(?:--platform=[^\s]+\s+)?(?P<image>[^\s:]+)(?::(?P<tag>[^\s]+))?(?:\s+as\s+[^\s]+)?'),
    re.compile(r'copy\s+--from=(?P<image>[^\s:]+)(?::(?P<tag>[^\s]+))?\s+.*'),
)
WORKFLOW_PATH = '.github/workflows/ci.yaml'


@dataclasses.dataclass
class Configuration:
    workdir: Path
    cache: Path
    options: dict[str, Any]

    @classmethod
    def load(cls, project: Path) -> Configuration:
        options = read_json(project/'default.json')
        options['registry']['password'] = os.environ.get('GITHUB_TOKEN')
        return cls(project, project/'.cache', options)

    def setup_cache(self) -> None:
        self.cache.mkdir(exist_ok=True)

    @property
    def authenticated(self) -> bool:
        return self.options['registry']['name'] and self.options['registry']['user'] and self.options['registry']['password']

    def registry_login(self) -> None:
        if self.authenticated:
            docker('login', self.options['registry']['name'], '--username', self.options['registry']['user'], '--password-stdin', stdin=self.options['registry']['password'])

    def registry_logout(self) -> None:
        if self.authenticated:
            docker('logout', self.options['registry']['name'], check=False)


@dataclasses.dataclass
class ContainerImage:
    context: Path
    dockerfile: Path

    @classmethod
    def from_file(cls, dockerfile: Path) -> ContainerImage:
        return cls(dockerfile.parent, dockerfile)

    @property
    def name(self) -> str:
        return '/'.join(item for item in (CONFIG.options['registry']['name'], CONFIG.options['registry']['user'], self.context.name) if item)

    def build(self, label_templates: dict[str, str], cache: bool = True) -> None:
        args = []
        if cache:
            args.extend((
                '--cache-from', f'type=local,src={CONFIG.cache}',
                '--cache-to', f'type=local,dest={CONFIG.cache}',
            ))
        for key, value in self._generate_image_labels(label_templates).items():
            args.extend(('--label', f'{key}={value}'))

        docker(
            'buildx', 'build',
            '--platform', 'linux/amd64',
            *args,
            '--tag', f'{self.name}:latest'
            '--push' if CONFIG.authenticated else '--load',
            '--file', self.dockerfile,
            self.context,
        )

    def _generate_image_labels(self, label_templates: dict[str, str]):
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        labels = {
            key: value.format(image=self, timestamp=timestamp)
            for key, value in label_templates.items()
        }
        labels = {
            key: value
            for key, value in labels.items()
            if value
        }
        return labels


def main() -> None:
    entrypoint = ArgumentParser()
    entrypoint.add_argument('-w', '--workdir', type=Path, default=Path.cwd(), metavar='DIR')
    subparsers = entrypoint.add_subparsers(dest='command', required=True)
    parser = subparsers.add_parser('image')
    parser.add_argument('image', nargs='+', type=Path, metavar='DOCKERFILE')
    parser.add_argument('--no-cache', action='store_const', const=True, default=False)
    parser = subparsers.add_parser('workflow')
    opts = entrypoint.parse_args()
    global CONFIG
    CONFIG = Configuration.load(opts.workdir)
    commands = dict(
        image=build_images,
        workflow=write_workflow,
    )
    commands[opts.command](opts)


def build_images(opts: Namespace) -> None:
    CONFIG.setup_cache()
    CONFIG.registry_login()
    try:
        for path in opts.image:
            image = ContainerImage.from_file(path)
            image.build(CONFIG.options['labels'], cache=not opts.no_cache)
    finally:
        CONFIG.registry_logout()


@dataclasses.dataclass
class Job:
    dockerfile: Path

    @classmethod
    def from_file(cls, dockerfile: Path) -> Job:
        return cls(dockerfile)

    @property
    def dependencies(self) -> list[str]:
        prefix = f'{CONFIG.options["registry"]["name"]}/{CONFIG.options["registry"]["user"]}/'
        return list(sorted(set(self._extract_dependencies(prefix))))

    @property
    def name(self) -> str:
        value = removesuffix(self.dockerfile.as_posix(), '/Dockerfile')
        value = removesuffix(value, '.Dockerfile')
        return value.replace('/', '-')

    def _extract_dependencies(self, prefix: str) -> Generator[str, None, None]:
        with open(self.dockerfile) as file:
            for line in file:
                image, tag = self._match_dependency_pattern(line)
                if image and image.startswith(prefix):
                    image_name = image.removeprefix(prefix)
                    path = Path(f'{image_name}/{tag}.Dockerfile')
                    yield f'{image_name}-{tag}' if path.is_file() else image_name

    @staticmethod
    def _match_dependency_pattern(line: str) -> tuple[Optional[str], Optional[str]]:
        for pattern in DOCKERFILE_DEPENDENCY_PATTERNS:
            match = pattern.fullmatch(line.strip().lower())
            if not match:
                continue
            return match.group('image'), match.group('tag')
        return None, None

    def generate(self) -> dict[str, Any]:
        return {
            'runs-on': 'ubuntu-24.04',
            'needs': self.dependencies,
            'steps': [
                {
                    'name': 'Checkout',
                    'uses': 'actions/checkout@v4',
                    'with': {
                        'fetch-depth': 0,
                    }
                },
                {
                    'name': 'Build, Test & Push',
                    'run': f'./build.py image {self.dockerfile}',
                    'env': {
                        'GITHUB_TOKEN': '${{ secrets.GITHUB_TOKEN }}'
                    },
                },
            ],
        }


def write_workflow(opts: Namespace) -> None:
    import yaml
    jobs = [
        Job.from_file(path.relative_to(opts.workdir))
        for path in sorted(opts.workdir.glob('*/Dockerfile'))
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
    sudo = () if 'docker' in groups else ('sudo', '--preserve-env=DOCKER_CLI_EXPERIMENTAL,BUILDX_NO_DEFAULT_LOAD,DOCKER_HOST')
    envvars = dict(DOCKER_CLI_EXPERIMENTAL='enabled', BUILDX_NO_DEFAULT_LOAD='false', DOCKER_HOST=os.environ.get('DOCKER_HOST', ''))
    return run(*sudo, 'docker', *args, env=envvars, **kwargs)


def git(*args: Any, **kwargs: Any) -> str:
    return run('git', *args, **kwargs)


def run(*args: Any, stdin: str|None = None, capture: bool = False, check: bool = True, env: dict[str, Any]|None = None) -> str:
    args = tuple(str(item) for item in args if item is not None)
    cmdline = ' '.join(args)
    print('>', cmdline, flush=True)
    environment = dict(os.environ, **env) if env else None
    process = subprocess.run(args, input=stdin, text=True, check=False, capture_output=capture, env=environment)
    if check and process.returncode != 0:
        message = f'{cmdline}: {process.stderr.strip()}' if process.stderr else cmdline
        raise RuntimeError(f'subprocess failed with exit code {process.returncode}: {message}')
    return process.stdout.strip() if capture else ''


def removesuffix(value: str, suffix: str) -> str:
    return value[:-len(suffix)] if value.endswith(suffix) else value


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


if __name__ == '__main__':
    main()

