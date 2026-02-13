ARG UBUNTU_VERSION=24.04
FROM docker.io/library/ubuntu:$UBUNTU_VERSION
ARG TIMEZONE=UTC
ARG LANGUAGE=en_US
ARG CHARSET=UTF-8
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
apt-get install --no-install-recommends -y ca-certificates locales tzdata wget && \
ln -sf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && \
localedef -i $LANGUAGE -c -f $CHARSET -A /usr/share/locale/locale.alias $LANGUAGE.$CHARSET && \
usermod ubuntu --home /dev/shm && \
rm -rf /home/ubuntu && \
mkdir -p /app/bin /app/lib /app/static /app/config /app/data && \
chown -R 1000:1000 /app
ENV HOME=/dev/shm
ENV XDG_RUNTIME_DIR=/dev/shm
ENV TMPDIR=/dev/shm
ENV LANG=$LANGUAGE.$CHARSET
ENV LANGUAGE=$LANGUAGE
ENV CHARSET=$CHARSET
ENV TZ=$TIMEZONE
WORKDIR /app
RUN apt-get update && \
apt-get install --no-install-recommends -y gnupg ca-certificates wget && \
wget -q -O - https://repo.jellyfin.org/ubuntu/jellyfin_team.gpg.key | apt-key add - && \
echo "deb [arch=$(dpkg --print-architecture)] https://repo.jellyfin.org/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") main" > /etc/apt/sources.list.d/jellyfin.list && \
apt-get purge --auto-remove --yes gnupg
RUN apt-get update && \
apt-get install --no-install-recommends -y jellyfin intel-media-va-driver-non-free && \
userdel --remove jellyfin && \
rm -f /etc/default/jellyfin /etc/init.d/jellyfin && \
rm -rf /usr/share/doc /etc/jellyfin /var/cache/jellyfin /var/log/jellyfin
COPY ./logging.json /app/config/
USER ubuntu
ENTRYPOINT ["jellyfin", "--configdir", "/app/config", "--datadir", "/app/data", "--cachedir", "/app/cache", "--logdir", "/dev/shm", "--webdir", "/usr/share/jellyfin/web", "--ffmpeg", "/usr/lib/jellyfin-ffmpeg/ffmpeg"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:8096/System/Info/Public"]
EXPOSE 8096/tcp
VOLUME /app/config /app/data /app/cache /app/media

