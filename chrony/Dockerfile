FROM ghcr.io/dadevel/cxx:dev as chrony
RUN apt-get update && apt-get install --no-install-recommends -y asciidoctor bison libcap-dev nettle-dev
COPY ./src .
# compiling without --enable-scfilter because starting chronyd with enforced seccomp filtering results in a crash
RUN ./configure \
--prefix=/app \
--bindir=/app/bin \
--sbindir=/app/bin \
--sysconfdir=/app/config \
--datarootdir=/app/static \
--localstatedir=/app/cache \
--chronyvardir=/app/cache \
--chronyrundir=/dev/shm \
--with-pidfile=/dev/shm/chronyd.pid \
--with-hwclockfile=/app/config/adjtime \
--with-sendmail=/usr/sbin/sendmail \
--with-user=app \
--disable-privdrop \
--enable-ntp-signd
RUN make -j $(nproc)
RUN strip ./chronyd ./chronyc
RUN setcap -q cap_net_bind_service,cap_sys_time+ep ./chronyd

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libcap2 libnettle8
COPY ./chrony.conf ./config/
COPY --from=chrony /build/chronyd /build/chronyc ./bin/
RUN chronyc --version
USER app
ENTRYPOINT ["chronyd", "-d", "-U", "-f", "./config/chrony.conf"]
CMD ["-L", "1", "-r", "-s"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["chronyc", "sources"]
EXPOSE 123/udp
VOLUME /app/config /app/cache
