FROM dadevel/go-builder:latest as receiver
COPY ./src/ .
RUN go build && strip ./alertmanager-signal-receiver

FROM dadevel/signal-cli:latest
USER root
RUN apk add --no-cache libgcc gcompat
COPY --from=receiver /build/alertmanager-signal-receiver ./bin/
USER app
ENTRYPOINT ["alertmanager-signal-receiver"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:9709/healthz"]
EXPOSE 9709/tcp

