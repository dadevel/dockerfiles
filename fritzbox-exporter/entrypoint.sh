#!/bin/sh
set -eu
export PASSWORD="$FRITZBOX_PASSWORD"
exec fritzbox-exporter -gateway-url "$FRITZBOX_API_URL" -gateway-luaurl "$FRITZBOX_WEB_URL" -username "$FRITZBOX_USERNAME" "$@"
