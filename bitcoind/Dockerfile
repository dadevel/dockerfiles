FROM ghcr.io/dadevel/cxx:dev as bitcoind
RUN apt-get update && apt-get install --no-install-recommends -y libboost-filesystem1.74-dev libboost-system1.74-dev libboost-thread1.74-dev libevent-dev libssl-dev autoconf automake libtool pkg-config
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

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libboost-filesystem1.74.0 libboost-system1.74 libboost-thread1.74.0 libevent-2.1-7 libevent-pthreads-2.1-7 libssl1.1 libgcc-s1
COPY ./bitcoin.conf ./config/
COPY --from=bitcoind /build/bitcoind /build/bitcoin-cli ./bin/
RUN bitcoind --version && bitcoin-cli --version
USER app
ENTRYPOINT ["bitcoind", "-conf=/app/config/bitcoin.conf", "-datadir=./data", "-nodebuglogfile", "-pid=/dev/shm/bitcoind.pid"]
CMD ["-listen", "-port=8333", "-server", "-rpcport=8332", "-rpcallowip=0.0.0.0/0", "-rpcallowip=::/0"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["bitcoin-cli", "-conf=/app/config/bitcoin.conf", "-datadir=./data", "ping"]
EXPOSE 8333/tcp 8332/tcp
