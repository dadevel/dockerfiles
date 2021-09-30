ARG MONO_VERSION=6
FROM docker.io/library/mono:$MONO_VERSION
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
apt-get install --no-install-recommends -y build-essential ca-certificates curl git libcap2-bin && \
ln -sf /usr/share/zoneinfo/UTC /etc/localtime
ENV LANG=C.UTF-8 \
CHARSET=UTF-8 \
TZ=UTC
WORKDIR /build
