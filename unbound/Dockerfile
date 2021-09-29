FROM ghcr.io/dadevel/cxx:dev as unbound
RUN apt-get update && apt-get install --no-install-recommends -y libexpat1-dev libssl-dev byacc file
COPY ./src .
RUN ./configure \
--prefix=/app \
--bindir=/app/bin \
--sbindir=/app/bin \
--libdir=/app/lib \
--sysconfdir=/app/config \
--sharedstatedir=/app/cache \
--localstatedir=/app/cache \
--datarootdir=/app/static \
--with-conf-file=/app/config/unbound.conf \
--with-run-dir= \
--with-pidfile= \
--with-username= \
--disable-systemd \
--without-pyunbound \
--without-pythonmodule \
--with-pthreads \
--enable-pie \
--enable-relro-now \
--with-pic \
--enable-flto \
--disable-rpath \
--enable-static-exe
RUN make -j $(nproc)
RUN strip ./unbound
RUN setcap -q cap_net_bind_service+ep ./unbound
RUN wget -q -O - https://www.internic.net/domain/named.cache | tee ./root.hints | awk '{ if ($3 == "A" || $3 == "AAAA") { printf("master: %s\n", $NF) } }' > ./root.conf && { ./unbound-anchor -a ./root.key -r ./root.hints || [ $? -eq 1 ]; }

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libssl1.1
COPY ./unbound.conf ./config/
COPY --from=unbound /build/unbound ./bin/
COPY --from=unbound --chown=app:app /build/root.hints /build/root.key /build/root.conf ./cache/
RUN unbound -V
USER app
ENTRYPOINT ["unbound", "-dd", "-c", "./config/unbound.conf"]
CMD ["-p"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nslookup", "health.unbound.test", "127.0.0.1"]
EXPOSE 53/tcp 53/udp 853/tcp
