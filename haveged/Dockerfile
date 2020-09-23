FROM dadevel/c-builder:latest as haveged
RUN apk add --no-cache autoconf automake file libtool linux-headers
COPY ./src .
RUN autoreconf -vif
RUN ./configure \
--prefix=/app \
--bindir=/app/bin \
--sbindir=/app/bin \
--libdir=/app/lib \
--sysconfdir=/app/config \
--sharedstatedir=/app/data \
--localstatedir=/app/data \
--datadir=/app/static \
--enable-static \
--disable-shared \
--with-pic
RUN make -j $(nproc) && strip ./src/haveged

FROM dadevel/alpine:latest
ARG TARGETARCH
RUN [ $TARGETARCH != arm ] || apk add --no-cache libgcc
COPY --from=haveged /build/src/haveged /app/bin/
RUN haveged --version
ENTRYPOINT ["haveged", "--Foreground", "--pidfile=/dev/shm/haveged.pid"]
CMD ["--verbose=1"]

