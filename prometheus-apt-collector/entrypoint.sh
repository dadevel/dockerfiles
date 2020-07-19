#!/bin/sh

TEXTFILE_DIR="${APT_COLLECTOR_TEXTFILE_DIR:-/app/data}"
ROOTFS="${APT_COLLECTOR_ROOTFS:-/rootfs}"
INTERVAL="${APT_COLLECTOR_INTERVAL:-3600}"

while :; do
    apt.sh > "$TEXTFILE_DIR/apt.prom.$$" && \
        mv "$TEXTFILE_DIR/apt.prom.$$" "$TEXTFILE_DIR/apt.prom" || \
        echo "error: metric collection failed with exit code $?"
    sleep "$INTERVAL"
done

