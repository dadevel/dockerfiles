#!/bin/sh
exec hostapd "$@" /app/config/*.conf

