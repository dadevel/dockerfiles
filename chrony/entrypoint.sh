#!/bin/sh
chown app:app /app/data/
exec chronyd "$@"

