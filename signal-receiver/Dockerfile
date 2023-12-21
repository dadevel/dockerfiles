FROM ghcr.io/dadevel/cxx:dev as signal-cli
RUN apt-get update && apt-get install --no-install-recommends -y dos2unix
RUN curl -sSI https://github.com/asamk/signal-cli/releases/latest | grep -i ^location: | dos2unix | grep -Eo '[0-9.]+$' | xargs -r -I {} curl -L 'https://github.com/asamk/signal-cli/releases/download/v{}/signal-cli-{}-linux-native.tar.gz' | tar -xzf - && chmod +x ./signal-cli

FROM ghcr.io/dadevel/go:dev as signal-receiver
COPY ./src .
RUN go build -o ./alertmanager-signal-receiver ./cmd/main.go
RUN strip ./alertmanager-signal-receiver

FROM ghcr.io/dadevel/debian:latest
# without this directory the dpkg install script of openjdk fails
RUN mkdir -p /usr/share/man/man1 && \
apt-get update && apt-get install --no-install-recommends -y openjdk-17-jre-headless
COPY --from=signal-cli /build/signal-cli ./bin/signal-cli
COPY --from=signal-receiver /build/alertmanager-signal-receiver ./bin/
USER app
ENTRYPOINT ["alertmanager-signal-receiver"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9709/healthz"]
EXPOSE 9709/tcp
VOLUME /app/data
