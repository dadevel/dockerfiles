FROM dadevel/cxx-builder:latest as bitcoind
RUN apk add --no-cache boost-dev libevent-dev libressl-dev autoconf automake libtool g++
COPY ./src .
ENV LC_ALL C
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
--disable-tests \
--disable-gui-tests \
--disable-bench \
--enable-suppress-external-warnings \
--enable-hardening \
--disable-wallet \
--enable-util-cli \
--with-gui=no \
--with-pic
RUN make -j $(nproc) && mv ./src/bitcoind ./src/bitcoin-cli .
RUN strip ./bitcoind ./bitcoin-cli
RUN ./bitcoind --version
RUN ./bitcoin-cli --version

FROM dadevel/alpine:latest
RUN apk add --no-cache boost-filesystem boost-system boost-thread libevent libressl libstdc++ libgcc
COPY --from=bitcoind /build/bitcoind /build/bitcoin-cli ./bin/
COPY ./bitcoin.conf ./config/
ENV LC_ALL C
USER app
ENTRYPOINT ["bitcoind", "-conf=/app/config/bitcoin.conf", "-datadir=./data", "-nodebuglogfile", "-pid=/dev/shm/bitcoind.pid"]
CMD ["-listen", "-port=8333", "-server", "-rpcport=8332", "-rpcallowip=0.0.0.0/0", "-rpcallowip=::/0"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["bitcoin-cli", "-conf=/app/config/bitcoin.conf", "-datadir=./data", "ping"]
EXPOSE 8333/tcp 8332/tcp

