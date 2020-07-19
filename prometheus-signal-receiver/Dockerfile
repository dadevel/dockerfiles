FROM gradle:jre14 as signal
WORKDIR /build
RUN git clone --depth 1 https://github.com/AsamK/signal-cli.git .
RUN ./gradlew build && ./gradlew installDist

FROM dadevel/go-builder:alpine as receiver
COPY ./src/ .
RUN go build && strip ./alertmanager-signal-receiver

FROM alpine:latest as alpine
RUN apk add --no-cache ca-certificates tzdata
RUN mkdir -p /app/bin /app/lib /app/static /app/config /app/data && \
chown -R 1000:1000 /app/data && \
chmod 0700 /app/data

FROM openjdk:14-alpine
ENV CHARSET UTF-8
ENV LANG C.UTF-8
ENV TZ UTC
COPY --from=alpine /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=alpine /usr/share/zoneinfo/UTC /etc/localtime
COPY --from=alpine /app /app
RUN addgroup -g 1000 app && adduser -h /app/data -g '' -s /bin/sh -G app -D -H -u 1000 app
ENV UID 1000
ENV GID 1000
ENV PATH /app/bin:$PATH
ENV LD_LIBRARY_PATH /app/lib
ENV HOME /app/data
ENV TMPDIR /tmp
WORKDIR /app
VOLUME /app/config /app/data
COPY --from=signal /build/build/install/signal-cli/bin/ ./bin/
COPY --from=signal /build/build/install/signal-cli/lib/ ./lib/
COPY --from=receiver /build/alertmanager-signal-receiver ./bin/
RUN apk add --no-cache libgcc gcompat
ENTRYPOINT ["alertmanager-signal-receiver"]
EXPOSE 9709/tcp
USER app:app

