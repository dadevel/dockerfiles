#!/bin/sh

TEXTFILE_DIR="${APT_COLLECTOR_TEXTFILE_DIR:-/app/data}"
INTERVAL="${APT_COLLECTOR_INTERVAL:-3600}"

while :; do
    if apt.sh > "$TEXTFILE_DIR/apt.prom.$$"; then
        mv "$TEXTFILE_DIR/apt.prom.$$" "$TEXTFILE_DIR/apt.prom"
        touch /dev/shm/health
    else
        echo "error: metric collection failed with exit code $?"
        rm -f /dev/shm/health
    fi
    sleep "$INTERVAL"
done

