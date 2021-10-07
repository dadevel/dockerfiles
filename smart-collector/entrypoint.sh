#!/bin/sh

INTERVAL="${SMART_COLLECTOR_INTERVAL:-3600}"
TEXT_FILE="${SMART_COLLECTOR_TEXTFILE_DIR:-/app/textfiles}/smart.prom"
TEMP_FILE="$TEXT_FILE.$$"
HEALTH_FILE=/dev/shm/healthy

while :; do
    if smartmon.py > "$TEMP_FILE"; then
        mv "$TEMP_FILE" "$TEXT_FILE"
        touch "$HEALTH_FILE"
    else
        echo "error: metric collection failed with exit code $?" >&2
        rm -f "$TEXT_FILE" "$HEALTH_FILE"
    fi
    sleep "$INTERVAL"
done
