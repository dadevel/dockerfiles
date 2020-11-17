FROM gradle:jre14 as signal
WORKDIR /build
COPY ./src/ .
RUN ./gradlew build && ./gradlew installDist

FROM dadevel/openjdk:latest
COPY --from=signal /build/build/install/signal-cli/bin/ ./bin/
COPY --from=signal /build/build/install/signal-cli/lib/ ./lib/
USER app
RUN signal-cli --version
ENTRYPOINT ["signal-cli"]
CMD ["--help"]

