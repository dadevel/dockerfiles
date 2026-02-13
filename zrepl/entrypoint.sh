#!/bin/sh
# zrepl requires a private directory for its socket
mkdir /dev/shm/zrepl/
chmod 0700 /dev/shm/zrepl/
exec zrepl daemon "$@"

