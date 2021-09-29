FROM ghcr.io/dadevel/go:dev as signal-receiver
COPY ./src .
RUN go build -o ./alertmanager-signal-receiver ./cmd/main.go
RUN strip ./alertmanager-signal-receiver

FROM ghcr.io/dadevel/signal-cli:latest
COPY --from=signal-receiver --chown=root:root /build/alertmanager-signal-receiver ./bin/
USER app
ENTRYPOINT ["alertmanager-signal-receiver"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9709/healthz"]
EXPOSE 9709/tcp
