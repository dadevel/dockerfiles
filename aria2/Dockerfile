FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache aria2
COPY ./entrypoint.sh /app/lib/
COPY ./aria2.conf /app/config/
USER app
ENTRYPOINT ["/app/lib/entrypoint.sh", "--log", "-", "--dir", "/app/downloads", "--save-session", "./downloads/session.lock", "--input-file", "/app/downloads/session.lock", "--conf-path", "/app/config/aria2.conf"]
CMD ["--enable-rpc", "--rpc-listen-all", "--rpc-listen-port", "6800"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nc", "-z", "localhost", "6800"]
EXPOSE 6800/tcp
VOLUME /app/config /app/downloads

