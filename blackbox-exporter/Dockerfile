FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache prometheus-blackbox-exporter
COPY ./blackbox-exporter.yaml /app/config/
USER app
ENTRYPOINT ["blackbox_exporter", "--config.file=/app/config/blackbox-exporter.yaml"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9115/"]
EXPOSE 9115/tcp
VOLUME /app/config

