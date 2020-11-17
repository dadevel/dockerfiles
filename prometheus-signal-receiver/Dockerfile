FROM gradle:jre14 as signal
WORKDIR /build
RUN git clone --depth 1 https://github.com/AsamK/signal-cli.git .
RUN ./gradlew build && ./gradlew installDist

FROM dadevel/go-builder:latest as receiver
COPY ./src/ .
RUN go build && strip ./alertmanager-signal-receiver

FROM dadevel/openjdk:latest
RUN apk add --no-cache libgcc gcompat
COPY --from=signal /build/build/install/signal-cli/bin/ ./bin/
COPY --from=signal /build/build/install/signal-cli/lib/ ./lib/
COPY --from=receiver /build/alertmanager-signal-receiver ./bin/
USER app
ENTRYPOINT ["alertmanager-signal-receiver"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "http://127.0.0.1:9709/healthz"]
EXPOSE 9709/tcp

