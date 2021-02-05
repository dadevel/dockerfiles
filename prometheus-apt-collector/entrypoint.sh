#!/bin/sh

TEXTFILE_DIR="${APT_COLLECTOR_TEXTFILE_DIR:-/app/cache}"
INTERVAL="${APT_COLLECTOR_INTERVAL:-3600}"

while :; do
    if apt.sh > "$TEXTFILE_DIR/apt.prom.$$"; then
        mv "$TEXTFILE_DIR/apt.prom.$$" "$TEXTFILE_DIR/apt.prom"
        touch /dev/shm/healthy
    else
        echo "error: metric collection failed with exit code $?" >&2
        rm -f /dev/shm/healthy
    fi
    sleep "$INTERVAL"
done

