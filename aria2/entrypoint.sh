#!/bin/sh
touch ./downloads/session.lock
exec aria2c "$@"
