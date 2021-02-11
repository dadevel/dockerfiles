FROM ghcr.io/dadevel/cxx-builder:latest as aria2
RUN apk add --no-cache libressl-dev libssh2-dev libxml2-dev zlib-dev c-ares-dev pkgconf autoconf automake gettext-dev libtool g++
COPY ./src .
RUN autoreconf --install --force
RUN ./configure \
--prefix=/app \
--bindir=/app/bin \
--sbindir=/app/bin \
--libdir=/app/lib \
--sysconfdir=/app/config \
--datarootdir=/app/static \
--sharedstatedir=/app/cache \
--localstatedir=/app/cache \
--runstatedir=/dev/shm \
--with-ca-bundle=/etc/ssl/certs/ca-certificates.crt \
--disable-nls \
--with-pic
RUN make -j $(nproc)
RUN mv ./src/aria2c ./aria2c
RUN strip ./aria2c
RUN ./aria2c --version

FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache libressl libssh2 libxml2 zlib c-ares libstdc++ libgcc
COPY --from=aria2 /build/aria2c ./bin/
COPY ./aria2.conf ./config/
USER app
ENTRYPOINT ["aria2c", "--log", "-", "--dir", "./storage", "--conf-path", "./config/aria2.conf", "--enable-rpc", "--rpc-listen-all"]
CMD ["--rpc-listen-port", "6800"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nc", "-z", "127.0.0.1", "6800"]
EXPOSE 6800/tcp

