FROM alpine:latest as alpine
RUN apk add --no-cache ca-certificates tzdata
RUN mkdir -p /app/bin /app/lib /app/static /app/config /app/data /app/cache /app/storage && \
chown -R 1000:1000 /app/data /app/cache /app/storage

FROM python:3-alpine
RUN addgroup -g 1000 app && adduser -h /dev/shm -g '' -s /bin/sh -G app -D -H -u 1000 app
ENV CHARSET UTF-8
ENV LANG C.UTF-8
ENV LC_ALL C
ENV TZ UTC
ENV PATH /app/bin:$PATH
ENV LD_LIBRARY_PATH /app/lib
ENV HOME /dev/shm
ENV XDG_RUNTIME_DIR /dev/shm
ENV TMPDIR /dev/shm
COPY --from=alpine /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=alpine /usr/share/zoneinfo/UTC /etc/localtime
COPY --from=alpine /app /app
WORKDIR /app
ENTRYPOINT ["/bin/sh"]
CMD ["-i"]

