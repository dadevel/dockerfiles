FROM ghcr.io/dadevel/ubuntu:latest
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
COPY ./logging.json ./config/
USER app
# jellyfin wants absolute paths
ENTRYPOINT ["jellyfin", "--configdir", "/app/data", "--datadir", "/app/data", "--cachedir", "/app/cache", "--logdir", "/dev/shm", "--webdir", "/usr/share/jellyfin/web", "--ffmpeg", "/usr/lib/jellyfin-ffmpeg/ffmpeg"]
# proper health check at /health endpoint throws 404
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:8096/System/Info/Public"]
EXPOSE 8096/tcp
