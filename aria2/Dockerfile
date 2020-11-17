FROM dadevel/c-builder:latest as aria2
RUN apk add --no-cache libressl-dev libssh2-dev libxml2-dev zlib-dev c-ares-dev pkgconf autoconf automake gettext-dev libtool g++
COPY ./src/ .
RUN autoreconf --force --install
RUN ./configure \
--prefix=/app \
--bindir=/app/bin \
--sbindir=/app/bin \
--libdir=/app/lib \
--sysconfdir=/app/config \
--datarootdir=/app/static \
--sharedstatedir=/app/data \
--localstatedir=/app/data \
--runstatedir=/dev/shm \
--with-ca-bundle=/etc/ssl/certs/ca-certificates.crt \
--disable-nls \
--with-pic
RUN make -j $(nproc) && strip ./src/aria2c

FROM dadevel/alpine:latest
RUN apk add --no-cache libressl libssh2 libxml2 zlib c-ares libstdc++ libgcc
COPY --from=aria2 /build/src/aria2c ./bin/
USER app
RUN aria2c --version
ENTRYPOINT ["aria2c", "--log", "-", "--dir", "./data", "--conf-path", "./config/aria2.conf", "--enable-rpc", "--rpc-listen-all"]
CMD ["--log-level", "warn", "--rpc-listen-port", "6800"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "http://127.0.0.1:6800"]
EXPOSE 6800/tcp

