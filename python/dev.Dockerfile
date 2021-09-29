ARG DEBIAN_VERSION=bullseye
ARG PYTHON_VERSION=3
FROM docker.io/library/python:$PYTHON_VERSION-slim-$DEBIAN_VERSION
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
apt-get install --no-install-recommends -y build-essential ca-certificates curl git libcap2-bin && \
ln -sf /usr/share/zoneinfo/UTC /etc/localtime
ENV LANG=C.UTF-8 \
CHARSET=UTF-8 \
TZ=UTC \
CFLAGS="-Os -pipe -flto -fstack-protector-strong --param=ssp-buffer-size=4 -fstack-clash-protection -fpie -fexceptions" \
CPPFLAGS="-D_FORTIFY_SOURCE=2 -D_GLIBCXX_ASSERTIONS" \
CXXFLAGS=$CFLAGS \
LDFLAGS="-Wl,-O1,-z,defs,-z,relro,-z,now,-pie,--hash-style=gnu,--no-copy-dt-needed-entries"
WORKDIR /build
