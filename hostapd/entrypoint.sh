#!/bin/sh
cat /app/config/*.conf > /dev/shm/hostapd.conf && \
    exec hostapd "$@" /dev/shm/hostapd.conf

