FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache alertmanager && mv /etc/alertmanager/alertmanager.yml /app/config/alertmanager.yaml
USER app
ENTRYPOINT ["alertmanager", "--config.file=/app/config/alertmanager.yaml", "--storage.path=/app/data"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9093/-/healthy"]
EXPOSE 9093/tcp
VOLUME /app/config /app/data

