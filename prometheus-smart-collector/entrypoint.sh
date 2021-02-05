#!/bin/sh

TEXTFILE_DIR="${SMARTMON_COLLECTOR_TEXTFILE_DIR:-/app/cache}"
INTERVAL="${SMARTMON_COLLECTOR_INTERVAL:-3600}"

while :; do
    if smartmon.py > "$TEXTFILE_DIR/smartmon.prom.$$"; then
        mv "$TEXTFILE_DIR/smartmon.prom.$$" "$TEXTFILE_DIR/smartmon.prom"
        touch /dev/shm/healthy
    else
        echo "error: metric collection failed with exit code $?" >&2
        rm -f /dev/shm/healthy
    fi
    sleep "$INTERVAL"
done

