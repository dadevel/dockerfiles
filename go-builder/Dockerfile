# explanation of compiler and linker options:
# https://wiki.debian.org/Hardening
# https://wiki.ubuntu.com/ToolChain/CompilerFlags
# https://security.stackexchange.com/questions/24444/what-is-the-most-hardened-set-of-options-for-gcc-compiling-c-c

FROM golang:alpine
RUN apk add --no-cache ca-certificates fortify-headers gcc git libcap make musl-dev patch tzdata && \
ln -s /usr/share/zoneinfo/UTC /etc/localtime
ENV CHARSET UTF-8
ENV LANG C.UTF-8
ENV LC_ALL C
ENV TZ UTC
ENV CFLAGS -Os -pipe -flto -fstack-protector-strong --param=ssp-buffer-size=4 -fstack-clash-protection -fpie -fexceptions
ENV CPPFLAGS -D_FORTIFY_SOURCE=2 -D_GLIBCXX_ASSERTIONS
ENV CXXFLAGS $CFLAGS
ENV LDFLAGS -Wl,-O1,-z,defs,-z,relro,-z,now,-pie,--hash-style=gnu,--no-copy-dt-needed-entries
# build fully static go binaries by default
ENV CGO_ENABLED 0
WORKDIR /build

