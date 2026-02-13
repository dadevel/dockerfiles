FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache hostapd
COPY ./entrypoint.sh /app/lib/
ENTRYPOINT ["/app/lib/entrypoint.sh", "-P", "/dev/shm/hostapd.pid", "-g", "/dev/shm/hostapd", "-G", "root"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["hostapd_cli", "-p", "/dev/shm/hostapd", "-s", "/dev/shm/hostapd", "quit"]
VOLUME /app/config

