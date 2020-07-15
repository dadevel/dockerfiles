#!/bin/sh

TEXTFILE_DIR="${SMARTMON_COLLECTOR_TEXTFILE_DIR:-/app/data}"
INTERVAL="${SMARTMON_COLLECTOR_INTERVAL:-3600}"

while :; do
    smartmon.py > "$TEXTFILE_DIR/smartmon.prom.$$" && \
        mv "$TEXTFILE_DIR/smartmon.prom.$$" "$TEXTFILE_DIR/smartmon.prom" || \
        echo "error: metric collection failed with exit code $?"
    sleep "$INTERVAL"
done

