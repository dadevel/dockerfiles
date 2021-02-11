FROM ghcr.io/dadevel/cxx-builder:latest as unbound
RUN apk add --no-cache expat-dev libressl-dev byacc file libcap
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
RUN ./unbound -V
RUN setcap -q cap_net_bind_service+ep ./unbound
# unbound-anchor exits with return code 1 even if everything went fine
RUN wget -q -O - https://www.internic.net/domain/named.cache | tee ./root.hints | awk '{ if ($3 == "A" || $3 == "AAAA") { printf("master: %s\n", $NF) } }' > ./root.conf && { ./unbound-anchor -a ./root.key -r ./root.hints || [ $? -eq 1 ]; }

FROM ghcr.io/dadevel/alpine:latest
COPY --from=unbound /build/unbound ./bin/
COPY --from=unbound --chown=app:app /build/root.hints /build/root.key /build/root.conf ./cache/
COPY ./unbound.conf ./config/
RUN apk add --no-cache libressl
USER 1000
ENTRYPOINT ["unbound", "-dd", "-c", "./config/unbound.conf"]
CMD ["-p"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nslookup", "health.unbound.test", "127.0.0.1"]
EXPOSE 53/tcp 53/udp 853/tcp

