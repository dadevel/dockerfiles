FROM gradle:jre14 as signal
WORKDIR /build
RUN git clone --depth 1 https://github.com/AsamK/signal-cli.git .
RUN ./gradlew build && ./gradlew installDist

FROM dadevel/go-builder:latest as receiver
COPY ./src/ .
RUN go build && strip ./alertmanager-signal-receiver

FROM alpine:latest as alpine
RUN apk add --no-cache ca-certificates tzdata
RUN mkdir -p /app/bin /app/lib /app/static /app/config /app/data && \
chown -R 1000:1000 /app/data

FROM openjdk:14-alpine
RUN apk add --no-cache libgcc gcompat && \
addgroup -g 1000 app && adduser -h /app/data -g '' -s /bin/sh -G app -D -H -u 1000 app
ENV CHARSET UTF-8
ENV LANG C.UTF-8
ENV TZ UTC
ENV UID 1000
ENV GID 1000
ENV PATH /app/bin:$PATH
ENV LD_LIBRARY_PATH /app/lib
ENV HOME /app/data
ENV TMPDIR /dev/shm
COPY --from=alpine /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=alpine /usr/share/zoneinfo/UTC /etc/localtime
COPY --from=alpine /app /app
COPY --from=signal /build/build/install/signal-cli/bin/ ./bin/
COPY --from=signal /build/build/install/signal-cli/lib/ ./lib/
COPY --from=receiver /build/alertmanager-signal-receiver ./bin/
ENTRYPOINT ["alertmanager-signal-receiver"]
WORKDIR /app
USER app
VOLUME /app/config /app/data
EXPOSE 9709/tcp

