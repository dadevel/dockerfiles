#!/bin/sh

TEXTFILE_DIR="${SMARTMON_COLLECTOR_TEXTFILE_DIR:-/app/data}"
INTERVAL="${SMARTMON_COLLECTOR_INTERVAL:-3600}"

while :; do
    if smartmon.py > "$TEXTFILE_DIR/smartmon.prom.$$"; then
        mv "$TEXTFILE_DIR/smartmon.prom.$$" "$TEXTFILE_DIR/smartmon.prom"
        touch /dev/shm/health
    else
        echo "error: metric collection failed with exit code $?"
        rm -f /dev/shm/health
    fi
    sleep "$INTERVAL"
done

