FROM dadevel/cxx-builder:latest as haveged
RUN apk add --no-cache autoconf automake file libtool linux-headers
COPY ./src .
RUN autoreconf -vif
RUN ./configure \
--prefix=/app \
--bindir=/app/bin \
--sbindir=/app/bin \
--libdir=/app/lib \
--sysconfdir=/app/config \
--datarootdir=/app/static \
--sharedstatedir=/app/cache \
--localstatedir=/app/cache \
--disable-shared \
--enable-static \
--with-pic
RUN make -j $(nproc)
RUN mv ./src/haveged .
RUN strip ./haveged
RUN ./haveged --version

FROM dadevel/alpine:latest
ARG TARGETARCH
RUN [ $TARGETARCH != arm ] || apk add --no-cache libgcc
COPY --from=haveged /build/haveged ./bin/
ENTRYPOINT ["haveged", "--Foreground", "--pidfile=/dev/shm/haveged.pid"]
CMD ["--verbose=1"]

