FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache prometheus
COPY ./prometheus.yaml /app/config/
USER app
ENTRYPOINT ["prometheus", "--config.file=/app/config/prometheus.yaml", "--storage.tsdb.path=/app/data", "--web.console.libraries=/app/config/console_libraries", "--web.console.templates=/app/config/consoles"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9090/-/healthy"]
EXPOSE 9090/tcp
VOLUME /app/config /app/data

