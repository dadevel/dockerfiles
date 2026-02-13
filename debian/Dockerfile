ARG DEBIAN_VERSION=trixie
FROM docker.io/library/debian:$DEBIAN_VERSION-slim
ARG PUID=1000
ARG PGID=1000
ARG TIMEZONE=UTC
ARG LANGUAGE=en_US
ARG CHARSET=UTF-8
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
apt-get install --no-install-recommends -y ca-certificates locales netcat-openbsd tzdata wget && \
ln -sf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && \
localedef -i $LANGUAGE -c -f $CHARSET -A /usr/share/locale/locale.alias $LANGUAGE.$CHARSET && \
groupadd --gid $PGID app && \
useradd --uid $PUID --gid $PGID --comment '' --home-dir /dev/shm --no-create-home --shell /bin/bash --no-log-init app && \
mkdir -p /app/bin /app/lib /app/static /app/config /app/data && \
chown -R $PUID:$PGID /app
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

