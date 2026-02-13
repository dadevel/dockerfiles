FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache wpa_supplicant
ENTRYPOINT ["wpa_supplicant", "-P", "/dev/shm/wpa-supplicant.pid", "-c", "./config/wpa-supplicant.conf"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wpa_cli", "-p", "/dev/shm/wpa-supplicant", "-s", "/dev/shm/wpa-supplicant", "quit"]
VOLUME /app/config

