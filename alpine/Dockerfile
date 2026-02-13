ARG ALPINE_VERSION=latest
FROM docker.io/library/alpine:$ALPINE_VERSION
ARG PUID=1000
ARG PGID=1000
ARG TIMEZONE=UTC
ARG LANGUAGE=en_US
ARG CHARSET=UTF-8
RUN addgroup -g $PGID app && adduser -D -u $PUID -G app -h /dev/shm -H app && \
mkdir -p /app /app/bin /app/lib /app/static /app/config /app/cache /app/data && chown -R $PUID:$PGID /app && \
apk add --no-cache libcap-setcap
ENV PATH=/app/bin:$PATH
ENV LD_LIBRARY_PATH=/app/lib
ENV HOME=/dev/shm
ENV XDG_RUNTIME_DIR=/dev/shm
ENV TMPDIR=/dev/shm
ENV LANG=$LANGUAGE.$CHARSET
ENV LANGUAGE=$LANGUAGE
ENV CHARSET=$CHARSET
ENV TZ=$TIMEZONE
WORKDIR /app

