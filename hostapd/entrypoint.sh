#!/bin/sh
[ -z "$HOSTAPD_TRANSMISSION_POWER_LIMIT" ] || iw "${HOSTAPD_INTERFACE:-phy0}" set txpower limit "$HOSTAPD_TRANSMISSION_POWER_LIMIT"
mkdir -p /dev/shm/hostapd && \
    cat ./config/*.conf > /dev/shm/hostapd.conf && \
    exec hostapd "$@" /dev/shm/hostapd.conf

