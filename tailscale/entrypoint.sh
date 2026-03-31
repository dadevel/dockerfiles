#!/bin/sh
set -e
tailscaled -no-logs-no-support -socks5-server "${TS_SOCKS5_SERVER:-127.0.0.1:1080}" -tun "${TS_TUN:-userspace-networking}" &
if [ -z "$TS_AUTHKEY" ] && [ -n "$TS_API_CLIENT_ID" ] && [ -n "$TS_API_CLIENT_SECRET" ] && [ -n "$TS_TAGS" ]; then
    TS_AUTHKEY="$(get-authkey -ephemeral -tags "$TS_TAGS")"
fi
tailscale up --auth-key="$TS_AUTHKEY" --hostname="$TS_HOSTNAME" --advertise-exit-node="${TS_EXIT_NODE:-true}" --ssh="${TS_SSH:-true}" --shields-up="${TS_SHIELDS_UP:-false}"
if [ -n "$TS_FWD_RHOST" ] && [ -n "$TS_FWD_RPORT" ]; then
    socat "tcp-listen:${TS_FWD_LPORT:-8080},reuseaddr,fork" "socks5-connect:${TS_SOCKS5_SERVER:-127.0.0.1:1080}:$TS_FWD_RHOST:$TS_FWD_RPORT" &
fi
wait
