FROM dadevel/go-builder:latest as signal-receiver
COPY ./src .
RUN go build
RUN strip ./alertmanager-signal-receiver

FROM dadevel/signal-cli:latest
COPY --from=signal-receiver --chown=root:root /build/alertmanager-signal-receiver ./bin/
USER app
ENTRYPOINT ["alertmanager-signal-receiver"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:9709/healthz"]
EXPOSE 9709/tcp

