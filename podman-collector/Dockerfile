FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache podman jq
COPY ./entrypoint.sh /app/lib/
ENV XDG_RUNTIME_DIR=/run
ENTRYPOINT ["/app/lib/entrypoint.sh"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["ls", "-d", "/dev/shm/healthy"]
VOLUME /app/textfiles

