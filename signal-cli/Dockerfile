FROM gradle:jre14 as signal-cli
WORKDIR /build
COPY ./src .
RUN ./gradlew build
RUN ./gradlew installDist
RUN ./build/install/signal-cli/bin/signal-cli --version

FROM openjdk:14-alpine
RUN apk add --no-cache libgcc gcompat && \
addgroup -g 1000 app && adduser -h /dev/shm -g '' -s /bin/sh -G app -D -H -u 1000 app
ENV CHARSET UTF-8
ENV LANG C.UTF-8
ENV LC_ALL C
ENV TZ UTC
ENV PATH /app/bin:$PATH
ENV LD_LIBRARY_PATH /app/lib
ENV HOME /dev/shm
ENV XDG_RUNTIME_DIR /dev/shm
ENV TMPDIR /dev/shm
COPY --from=dadevel/alpine /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=dadevel/alpine /etc/localtime /etc/localtime
COPY --from=dadevel/alpine /app /app
WORKDIR /app
COPY --from=signal-cli /build/build/install/signal-cli/bin/ ./bin/
COPY --from=signal-cli /build/build/install/signal-cli/lib/ ./lib/
ENTRYPOINT ["signal-cli"]
CMD ["--help"]

