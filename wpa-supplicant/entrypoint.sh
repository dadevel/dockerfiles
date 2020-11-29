#!/bin/sh
mkdir -p /dev/shm/wpa-supplicant && \
    exec wpa_supplicant "$@"

