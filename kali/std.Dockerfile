FROM docker.io/kalilinux/kali-rolling:latest
ARG TIMEZONE=UTC
ARG LANGUAGE=en_US
ARG CHARSET=UTF-8
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
apt-get install --no-install-recommends -y ca-certificates locales tzdata && \
ln -sf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && \
localedef -i $LANGUAGE -c -f $CHARSET -A /usr/share/locale/locale.alias $LANGUAGE.$CHARSET
ENV LANG=$LANGUAGE.$CHARSET \
LANGUAGE=$LANGUAGE \
CHARSET=$CHARSET \
TZ=$TIMEZONE
WORKDIR /workdir
COPY ./std.txt ./pkgs.txt
RUN grep -v -e '^#' -e '^$' ./pkgs.txt | xargs -r -- apt-get install --no-install-recommends -y --
