#!/bin/sh
mkdir -p ./downloads
touch ./downloads/session.lock
exec aria2c "$@"
