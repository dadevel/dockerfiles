FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache haveged
ENTRYPOINT ["haveged", "--Foreground", "--pidfile=/dev/shm/haveged.pid"]
CMD ["--verbose=1"]

