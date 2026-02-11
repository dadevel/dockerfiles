FROM ghcr.io/dadevel/cxx:dev AS haveged
RUN apt-get update && apt-get install --no-install-recommends -y autoconf automake file libtool linux-headers-generic
COPY ./src .
RUN autoreconf -vif
RUN ./configure \
--prefix=/app \
--bindir=/app/bin \
--sbindir=/app/bin \
--libdir=/app/lib \
--sysconfdir=/app/config \
--datarootdir=/app/static \
--sharedstatedir=/app/data \
--localstatedir=/app/data \
--disable-shared \
--enable-static \
--with-pic
RUN make -j $(nproc)
RUN mv ./src/haveged .
RUN strip ./haveged

FROM ghcr.io/dadevel/debian:latest
COPY --from=haveged /build/haveged ./bin/
RUN haveged --version || [ $? -eq 1 ]
ENTRYPOINT ["haveged", "--Foreground", "--pidfile=/dev/shm/haveged.pid"]
CMD ["--verbose=1"]
