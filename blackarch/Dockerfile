FROM docker.io/library/archlinux:base
ARG PUID=1000
ARG PGID=1000
ARG TIMEZONE=UTC
ARG LANGUAGE=en_US
ARG CHARSET=UTF-8
COPY ./sudoers /etc/sudoers
RUN chmod 440 /etc/sudoers && \
pacman -Syu --needed --noconfirm ca-certificates curl filesystem sudo tzdata && \
ln -sf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && \
localedef -i $LANGUAGE -c -f $CHARSET -A /usr/share/locale/locale.alias $LANGUAGE.$CHARSET && \
groupadd --gid $PGID app && \
useradd --uid $PUID --gid $PGID --groups wheel --comment '' --home-dir /home/app --create-home --shell /bin/bash --no-log-init app && \
export TERM=xterm && \
curl -sS https://blackarch.org/strap.sh | bash
COPY ./entrypoint.sh /
WORKDIR /home/app
ENV HOME=/home/app \
XDG_RUNTIME_DIR=/run/user/$PUID \
TMPDIR=/dev/shm \
LANG=$LANGUAGE.$CHARSET \
LANGUAGE=$LANGUAGE \
CHARSET=$CHARSET \
TZ=$TIMEZONE
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash", "-i"]
