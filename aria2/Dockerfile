FROM dadevel/c-builder:latest as aria2
RUN apk add --no-cache openssl-dev libssh2-dev libxml2-dev zlib-dev c-ares-dev pkgconf autoconf automake gettext-dev libtool g++
COPY ./src .
RUN autoreconf --force --install
RUN ./configure \
--prefix=/app \
--sbindir=/app/bin \
--sysconfdir=/app/config \
--localstatedir=/app/data \
--runstatedir=/dev/shm \
--with-ca-bundle=/etc/ssl/certs/ca-certificates.crt \
--disable-nls \
--with-pic
RUN make -j $(nproc) && strip ./src/aria2c

FROM dadevel/alpine:latest
RUN apk add --no-cache openssl libssh2 libxml2 zlib c-ares libstdc++ libgcc
COPY --from=aria2 /build/src/aria2c /app/bin/
RUN aria2c --version
USER app
ENTRYPOINT ["aria2c", "--log", "-", "--enable-rpc", "--rpc-listen-all"]
CMD ["--log-level", "warn", "--dir", "/app/data", "--conf-path", "/app/config/aria2.conf", "--rpc-listen-port", "6800"]
EXPOSE 6800/tcp

