#!/bin/sh

RELOAD_COMMAND="${LEGO_RELOAD_COMMAND:-}"
RENEW_INTERVAL="${LEGO_RENEW_INTERVAL:-7d}"

while :; do
    if [ "$(lego "$@" list)" = "No certificates found." ]; then
        lego "$@" run --must-staple && sh -c "$RELOAD_COMMAND"
    else
        lego "$@" renew --must-staple --reuse-key --days 30 && sh -c "$RELOAD_COMMAND"
    fi
    sleep "$RENEW_INTERVAL"
done

