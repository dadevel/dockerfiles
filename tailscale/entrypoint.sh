#!/bin/sh
set -eu
tailscaled -no-logs-no-support -socks5-server 127.0.0.1:1080 -tun userspace-networking &
tailscale up --auth-key="$TS_AUTHKEY" --hostname="${TS_HOSTNAME:-}" --advertise-exit-node="${TS_EXIT_NODE:-true}" --ssh="${TS_SSH:-true}" --shields-up="${TS_SHIELDS_UP:-false}"
if [ -n "${TS_FWD_HOST:-}" ] && [ -n "${TS_FWD_PORT:-}" ]; then
    socat tcp-listen:8080,reuseaddr,fork socks5-connect:127.0.0.1:1080:"$TS_FWD_HOST:$TS_FWD_PORT" &
fi
wait
