#!/bin/sh
[ "$(stat -c %U:%G /app/data/)" = app:app ] || chown -R app:app /app/data/
exec chronyd "$@"

