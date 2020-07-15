FROM alpine:latest
RUN apk add --no-cache ca-certificates fortify-headers gcc git make musl-dev patch tzdata && \
ln -s /usr/share/zoneinfo/UTC /etc/localtime
ENV CHARSET UTF-8
ENV LANG C.UTF-8
ENV TZ UTC
# flags taken from https://wiki.debian.org/Hardening, https://wiki.ubuntu.com/ToolChain/CompilerFlags and https://security.stackexchange.com/questions/24444/what-is-the-most-hardened-set-of-options-for-gcc-compiling-c-c
ENV CFLAGS -Os -pipe -flto -fstack-protector-strong --param=ssp-buffer-size=4 -fstack-clash-protection -fexceptions -fpie
ENV CPPFLAGS -D_FORTIFY_SOURCE=2 -D_GLIBCXX_ASSERTIONS
ENV CXXFLAGS $CFLAGS
ENV LDFLAGS -Wl,-O1,-z,defs,-z,relro,-z,now,-pie,--hash-style=gnu,--no-copy-dt-needed-entries
WORKDIR /build

