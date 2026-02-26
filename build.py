#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from typing import Any, Generator

import dataclasses
import re

import yaml


def main() -> None:
    workdir = Path.cwd()
    jobs = [
        Job.from_file(path.relative_to(workdir))
        for path in sorted(workdir.glob('*/Dockerfile'))
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
    workdir.joinpath('.github/workflows/ci.yaml').write_text(text)


DOCKERFILE_DEPENDENCY_PATTERNS = (
    re.compile(r'from\s+(?:--platform=[^\s]+\s+)?(?P<image>[^\s:]+)(?::(?P<tag>[^\s]+))?(?:\s+as\s+[^\s]+)?'),
    re.compile(r'copy\s+--from=(?P<image>[^\s:]+)(?::(?P<tag>[^\s]+))?\s+.*'),
)

@dataclasses.dataclass
class Job:
    dockerfile: Path

    @classmethod
    def from_file(cls, dockerfile: Path) -> Job:
        return cls(dockerfile)

    @property
    def context(self) -> str:
        return self.dockerfile.parent.as_posix()

    @property
    def name(self) -> str:
        return self.dockerfile.parent.name

    @property
    def dependencies(self) -> list[str]:
        prefix = f'ghcr.io/dadevel/'
        return list(sorted(set(self._extract_dependencies(prefix))))

    def _extract_dependencies(self, prefix: str) -> Generator[str]:
        with open(self.dockerfile) as file:
            for line in file:
                image, tag = self._match_dependency_pattern(line)
                if image and image.startswith(prefix):
                    image_name = image.removeprefix(prefix)
                    path = Path(f'{image_name}/{tag}.Dockerfile')
                    yield f'{image_name}-{tag}' if path.is_file() else image_name

    @staticmethod
    def _match_dependency_pattern(line: str) -> tuple[str|None, str|None]:
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
                    'name': 'Git Checkout',
                    'uses': 'actions/checkout@v5',
                    'with': {
                        'fetch-depth': 0,
                    }
                },
                {
                    'name': 'Docker Setup',
                    'uses': 'docker/setup-buildx-action@v3',
                },
                {
                    'name': 'Docker Login',
                    'uses': 'docker/login-action@v3',
                    'with': {
                        'registry': 'ghcr.io',
                        'username': 'dadevel',
                        'password': '${{ secrets.GITHUB_TOKEN }}',
                    }
                },
                {
                    'name': 'Docker Build & Push',
                    'uses': 'docker/build-push-action@v6',
                    'with': {
                        'context': self.context,
                        'tags': f'ghcr.io/dadevel/{self.name}:latest',
                        'labels': f'org.opencontainers.image.title={self.name}\norg.opencontainers.image.author=dadevel\norg.opencontainers.image.source=https://github.com/dadevel/dockerfiles\n',
                        'push': True,
                    },
                },
            ],
        }


def str_presenter(dumper: yaml.representer.SafeRepresenter, data: str) ->  yaml.ScalarNode:
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


if __name__ == '__main__':
    main()

