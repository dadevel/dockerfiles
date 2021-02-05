FROM dadevel/cxx-builder:latest as chrony
RUN apk add --no-cache asciidoctor bison libcap-dev nettle-dev
COPY ./src .
# compiling without --enable-scfilter because starting chronyd with enforced seccomp filtering results in a crash
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
--with-hwclockfile=/app/static/adjtime \
--with-sendmail=/usr/sbin/sendmail \
--with-user=app \
--disable-privdrop \
--enable-ntp-signd
RUN make -j $(nproc)
RUN strip ./chronyd ./chronyc
RUN ./chronyd --version
RUN setcap -q cap_net_bind_service,cap_sys_time+ep ./chronyd

FROM dadevel/alpine:latest
ARG TARGETARCH
RUN apk add --no-cache libcap nettle && [ $TARGETARCH != arm ] || apk add --no-cache libgcc
COPY --from=chrony /build/chronyd ./bin/
COPY --from=chrony /build/chronyc ./bin/
COPY ./chrony.conf ./config/
USER app
ENTRYPOINT ["chronyd", "-d", "-U", "-f", "./config/chrony.conf"]
CMD ["-L", "1", "-r", "-s"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["chronyc", "sources"]
EXPOSE 123/udp

