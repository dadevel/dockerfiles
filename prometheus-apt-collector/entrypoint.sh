#!/bin/sh

TEXTFILE_DIR="${APT_COLLECTOR_TEXTFILE_DIR:-/app/data}"
INTERVAL="${APT_COLLECTOR_INTERVAL:-3600}"
export ROOTFS="${APT_COLLECTOR_ROOTFS:-/rootfs}"

while :; do
    apt.sh > "$TEXTFILE_DIR/apt.prom.$$" && \
        mv "$TEXTFILE_DIR/apt.prom.$$" "$TEXTFILE_DIR/apt.prom" || \
        echo "error: metric collection failed with exit code $?"
    sleep "$INTERVAL"
done

