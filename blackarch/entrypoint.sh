#!/usr/bin/env bash
[[ "$PUID" == "$(id -u app)" && "$PGID" == "$(id -g app)" ]] || usermod --uid "$PUID" --gid "$PGID" app
exec sudo -u app -- "$@"
