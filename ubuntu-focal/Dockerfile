FROM ubuntu:focal as ubuntu
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install --no-install-recommends --yes ca-certificates tzdata
RUN mkdir -p /app/bin /app/lib /app/static /app/config /app/data /app/cache /app/storage && \
chown -R 1000:1000 /app/data /app/cache /app/storage

FROM ubuntu:focal
RUN useradd --uid 1000 --user-group --home-dir /dev/shm --no-create-home --no-log-init app
ENV CHARSET UTF-8
ENV LANG C.UTF-8
ENV LC_ALL C
ENV TZ UTC
ENV PATH /app/bin:$PATH
ENV LD_LIBRARY_PATH /app/lib
ENV HOME /dev/shm
ENV XDG_RUNTIME_DIR /dev/shm
ENV TMPDIR /dev/shm
ENV DEBIAN_FRONTEND noninteractive
COPY --from=ubuntu /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=ubuntu /usr/share/zoneinfo/UTC /etc/localtime
COPY --from=ubuntu /app /app
WORKDIR /app

