#!/bin/sh

[ -z "$OPENCONNECT_TOKEN_SECRET" ] || echo -n "$OPENCONNECT_TOKEN_SECRET" > /dev/shm/secret.txt
sleep 45 && rm -f /dev/shm/secret.txt &

[ -n "$OPENCONNECT_ENDPOINT" ] || read -r -p 'Endpoint URL: ' OPENCONNECT_ENDPOINT
[ -n "$OPENCONNECT_USER" ] || read -r -p 'Username: ' OPENCONNECT_USER
[ -n "$OPENCONNECT_PROTOCOL" ] || read -r -p 'Protocol: ' OPENCONNECT_PROTOCOL

[ -z "$OPENCONNECT_INTERFACE" ] || set -- "$@" --interface "$OPENCONNECT_INTERFACE"
[ -z "$OPENCONNECT_TOKEN_MODE" ] || set -- "$@" --token-mode "$OPENCONNECT_TOKEN_MODE"
[ -z "$OPENCONNECT_TOKEN_SECRET" ] || set -- "$@" --token-secret @/dev/shm/secret.txt

set -- "$@" \
    --protocol "$OPENCONNECT_PROTOCOL" \
    --user "$OPENCONNECT_USER" \
    --csd-wrapper /app/lib/tncc-emulate.py \
    --csd-user nobody \
    --useragent "${OPENCONNECT_USER_AGENT:-Mozilla/5.0 (Linux) Firefox}" \
    --local-hostname "${OPENCONNECT_HOSTNAME:-localhost}"

if [ -n "$OPENCONNECT_PASSWORD" ]; then
    echo "$OPENCONNECT_PASSWORD" | openconnect --passwd-on-stdin "$@" "$OPENCONNECT_ENDPOINT"
else
    openconnect "$@" "$OPENCONNECT_ENDPOINT"
fi
