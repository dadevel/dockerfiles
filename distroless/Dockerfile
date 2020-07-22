FROM alpine:latest as alpine
RUN apk add --no-cache ca-certificates tzdata
RUN mkdir -p /app/bin /app/lib /app/static /app/config /app/data && \
chown -R 1000:1000 /app/data

FROM scratch
ENV CHARSET UTF-8
ENV LANG C.UTF-8
ENV TZ UTC
COPY --from=alpine /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=alpine /usr/share/zoneinfo/UTC /etc/localtime
COPY --from=alpine /app /app
COPY --from=alpine /tmp /tmp
ENV UID 1000
ENV GID 1000
ENV PATH /app/bin
ENV LD_LIBRARY_PATH /app/lib
ENV HOME /app/data
ENV TMPDIR /dev/shm
WORKDIR /app
VOLUME /app/config /app/data

