FROM debian:stable-slim as debian
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install --no-install-recommends --yes ca-certificates tzdata
RUN mkdir -p /app/bin /app/lib /app/static /app/config /app/data && \
chown -R 1000:1000 /app/data

FROM debian:stable-slim
RUN useradd --uid 1000 --user-group --home-dir /dev/shm --no-create-home --no-log-init app
ENV CHARSET UTF-8
ENV LANG C.UTF-8
ENV TZ UTC
ENV PATH /app/bin:$PATH
ENV LD_LIBRARY_PATH /app/lib
ENV HOME /dev/shm
ENV XDG_RUNTIME_DIR /dev/shm
ENV TMPDIR /dev/shm
ENV DEBIAN_FRONTEND noninteractive
COPY --from=debian /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=debian /usr/share/zoneinfo/UTC /etc/localtime
COPY --from=debian /app /app
WORKDIR /app

