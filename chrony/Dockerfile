FROM dadevel/c-builder:latest as chrony
# compiling with --disable-privdrop and managing privileges via docker does not work, chrony insists on starting as root
# not installing libseccomp and specifying --enable-scfilter because starting chronyd with -F 1 to enforce seccomp filtering only results in a crash
RUN apk add --no-cache asciidoctor bison gnutls-dev libcap-dev nettle-dev
COPY ./src .
RUN ./configure \
--prefix=/app \
--bindir=/app/bin \
--sbindir=/app/bin \
--sysconfdir=/app/config \
--datarootdir=/app/static \
--localstatedir=/app/data \
--chronyvardir=/app/data \
--chronyrundir=/dev/shm \
--with-pidfile=/dev/shm/chronyd.pid \
--with-hwclockfile=/app/data/adjtime \
--with-user=app \
--with-sendmail=/usr/sbin/sendmail \
--enable-ntp-signd
RUN make -j $(nproc) && strip ./chronyd

FROM dadevel/alpine:latest
COPY --from=chrony /build/chronyd /app/bin/
RUN apk add --no-cache gnutls libcap nettle && chronyd -v
ENTRYPOINT ["chronyd", "-d"]
CMD ["-u", "app", "-f", "/app/config/chrony.conf", "-r", "-s"]
EXPOSE 123/udp

