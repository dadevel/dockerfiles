FROM dadevel/c-builder:latest as unbound
# fstrm and protobuf are required for dnstap
RUN apk add --no-cache expat-dev expat-static file fstrm-dev fstrm-static libevent-dev libevent-static libressl-dev protobuf-c-dev
COPY ./src .
RUN ./configure \
--prefix=/app \
--bindir=/app/bin \
--sbindir=/app/bin \
--libdir=/app/lib \
--sysconfdir=/app/config \
--sharedstatedir=/app/data \
--localstatedir=/app/data \
--datarootdir=/app/static \
--with-conf-file=/app/config/unbound.conf \
--with-run-dir= \
--with-pidfile= \
--with-username= \
--disable-rpath \
--with-pthreads \
--with-libevent \
--enable-event-api \
--enable-dnstap \
--enable-static \
--enable-static-exe \
--enable-fully-static \
--disable-flto \
--enable-pie \
--enable-relro-now \
--with-pic
# additional feature flags
# --enable-tfo-client --enable-tfo-server --enable-ipset --enable-subnet
RUN make -j $(nproc) && \
strip ./unbound && \
setcap -q cap_net_bind_service+ep ./unbound
# unbound-anchor exits with return code 1 even if everything went fine
RUN wget -q -O - https://www.internic.net/domain/named.cache | tee ./root.hints | awk '{ if ($3 == "A" || $3 == "AAAA") { printf("master: %s\n", $NF) } }' > ./root.conf && { ./unbound-anchor -a ./root.key -r ./root.hints || [ $? -eq 1 ]; }

FROM dadevel/distroless:latest
COPY --from=unbound /build/unbound /app/bin/
COPY --from=unbound --chown=1000:1000 /build/root.hints /build/root.key /build/root.conf /app/data/
RUN ["unbound", "-V"]
ENTRYPOINT ["unbound", "-dd"]
CMD ["-p", "-c", "/app/config/unbound.conf"]
USER 1000
EXPOSE 53/tcp 53/udp 853/tcp

