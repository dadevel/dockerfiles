FROM dadevel/cxx-builder:latest as dnsmasq
RUN apk add --no-cache gettext libidn2-dev libnetfilter_conntrack-dev linux-headers musl-libintl nettle-dev
COPY ./src ./config.patch .
RUN patch -u -i ./config.patch ./src/config.h
RUN make -j $(nproc) all-i18n && mv ./src/dnsmasq .
RUN strip ./dnsmasq
RUN ./dnsmasq --version

FROM dadevel/alpine:latest
# root must own ./data because dnsmasq accesses ./data/leases before switching user
RUN apk add --no-cache libidn2 libnetfilter_conntrack nettle && chown -R root:root ./data/
COPY --from=dnsmasq /build/dnsmasq ./bin/
COPY --from=dnsmasq /build/trust-anchors.conf ./static/
COPY ./dnsmasq.conf ./hosts ./resolv.conf ./config/
ENTRYPOINT ["dnsmasq", "--keep-in-foreground", "--log-facility=-", "--user=app", "--group=app", "--pid-file=", "--conf-file=./config/dnsmasq.conf", "--host-record=health.dnsmasq.test,127.0.0.1"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nslookup", "health.dnsmasq.test", "127.0.0.1"]
EXPOSE 53/udp 67/udp 69/udp 547/udp
STOPSIGNAL SIGTERM

