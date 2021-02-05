FROM dadevel/cxx-builder:latest as bitcoind
RUN apk add --no-cache boost-dev libevent-dev libressl-dev autoconf automake libtool g++
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
--disable-tests \
--disable-gui-tests \
--disable-bench \
--disable-wallet \
--with-gui=no \
--enable-suppress-external-warnings \
--enable-hardening \
--enable-util-cli \
--with-pic
RUN make -j $(nproc)
RUN mv ./src/bitcoind ./src/bitcoin-cli .
RUN strip ./bitcoind ./bitcoin-cli
RUN ./bitcoind --version
RUN ./bitcoin-cli --version

FROM dadevel/alpine:latest
RUN apk add --no-cache boost-filesystem boost-system boost-thread libevent libressl libstdc++ libgcc
COPY --from=bitcoind /build/bitcoind /build/bitcoin-cli ./bin/
COPY ./bitcoin.conf ./config/
USER app
ENTRYPOINT ["bitcoind", "-conf=/app/config/bitcoin.conf", "-datadir=./data", "-nodebuglogfile", "-pid=/dev/shm/bitcoind.pid"]
CMD ["-listen", "-port=8333", "-server", "-rpcport=8332", "-rpcallowip=0.0.0.0/0", "-rpcallowip=::/0"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["bitcoin-cli", "-conf=/app/config/bitcoin.conf", "-datadir=./data", "ping"]
EXPOSE 8333/tcp 8332/tcp

