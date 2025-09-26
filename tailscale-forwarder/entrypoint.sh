#!/bin/sh
set -eu
echo 'starting tailscaled' >&2
tailscaled -no-logs-no-support -socket=/dev/shm/tailscaled.sock -statedir=/var/lib/tailscale -socks5-server=:1080 -tun=userspace-networking &
echo 'bringing tailscale up' >&2
tailscale --socket=/dev/shm/tailscaled.sock up --login-server="${TS_LOGIN_SERVER:-https://controlplane.tailscale.com}" --timeout="${TS_TIMEOUT:-10s}" --auth-key="${TS_AUTHKEY:?undefined}" --hostname="${TS_HOSTNAME:-$HOSTNAME}" --accept-dns="${TS_ACCEPT_DNS:-true}" --accept-routes="${TS_ACCEPT_ROUTES:-false}" --advertise-exit-node="${TS_ADVERTISE_EXIT_NODE:-false}" --ssh="${TS_SSH:-false}" --shields-up="${TS_SHIELDS_UP:-true}" "$@"
echo 'running socat' >&2
socat "tcp-listen:8080,reuseaddr,fork,max-children=${UPSTREAM_MAX_CONNECTIONS:-16}" "socks5-connect:127.0.0.1:1080:${UPSTREAM_HOST:?undefined}:${UPSTREAM_PORT:?undefined}"
