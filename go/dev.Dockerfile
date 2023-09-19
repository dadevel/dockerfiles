ARG GOLANG_VERSION=1
ARG DEBIAN_VERSION=bookworm
FROM golang:$GOLANG_VERSION-$DEBIAN_VERSION
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
apt-get install --no-install-recommends -y build-essential ca-certificates curl git libcap2-bin && \
ln -sf /usr/share/zoneinfo/UTC /etc/localtime
ENV LANG=C.UTF-8 \
CHARSET=UTF-8 \
TZ=UTC \
CFLAGS="-Os -pipe -flto -fstack-protector-strong --param=ssp-buffer-size=4 -fstack-clash-protection -fpie -fexceptions -fasynchronous-unwind-tables" \
CPPFLAGS="-D_FORTIFY_SOURCE=2 -D_GLIBCXX_ASSERTIONS" \
CXXFLAGS=$CFLAGS \
LDFLAGS="-Wl,-O1,-z,defs,-z,relro,-z,now,-pie,--hash-style=gnu,--no-copy-dt-needed-entries" \
CGO_ENABLED=0
WORKDIR /build
