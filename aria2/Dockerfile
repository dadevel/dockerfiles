FROM ghcr.io/dadevel/cxx:dev as aria2
RUN apt-get update && apt-get install --no-install-recommends -y libssl-dev libssh2-1-dev libxml2-dev zlib1g-dev libc-ares-dev pkgconf autoconf automake autopoint gettext libtool
COPY ./src .
RUN autoreconf --install --force
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
RUN make -j $(nproc)
RUN mv ./src/aria2c ./aria2c
RUN strip ./aria2c

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libssl3 libssh2-1 libxml2 zlib1g libc-ares2
COPY entrypoint.sh ./lib/
COPY ./aria2.conf ./config/
COPY --from=aria2 /build/aria2c ./bin/
RUN aria2c --version
USER app
ENTRYPOINT ["./lib/entrypoint.sh", "--log", "-", "--dir", "./downloads", "--save-session", "./downloads/session.lock", "--input-file", "./downloads/session.lock", "--conf-path", "./config/aria2.conf"]
CMD ["--enable-rpc", "--rpc-listen-all", "--rpc-listen-port", "6800"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nc", "-z", "localhost", "6800"]
EXPOSE 6800/tcp
VOLUME /app/config /app/downloads
