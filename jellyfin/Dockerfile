FROM ubuntu:focal
ENV CHARSET UTF-8
ENV LANG C.UTF-8
ENV TZ UTC
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
apt-get install --no-install-recommends --yes gnupg ca-certificates wget && \
wget -q -O - https://repo.jellyfin.org/ubuntu/jellyfin_team.gpg.key | apt-key add - && \
echo "deb [arch=$(dpkg --print-architecture)] https://repo.jellyfin.org/ubuntu focal main" > /etc/apt/sources.list.d/jellyfin.list && \
apt-get purge --auto-remove --yes gnupg
RUN apt-get update && \
apt-get install --no-install-recommends --yes jellyfin intel-media-va-driver-non-free && \
userdel --remove jellyfin && \
rm -rf /usr/share/doc
RUN useradd --uid 1000 --user-group --home-dir /dev/shm --no-create-home --shell /usr/bin/bash app && \
mkdir -p /app/config /app/data /app/cache && \
chown -R app:app /app/config /app/data /app/cache
COPY ./logging.json /app/config/
USER app
WORKDIR /app
# jellyfin wants absolute paths
ENTRYPOINT ["jellyfin", "--configdir", "/app/data", "--datadir", "/app/data", "--cachedir", "/app/cache", "--logdir", "/dev/shm", "--webdir", "/usr/share/jellyfin/web", "--ffmpeg", "/usr/lib/jellyfin-ffmpeg/ffmpeg"]
# proper health check at /health endpoint throws 404
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:8096/System/Info/Public"]
EXPOSE 8096/tcp

