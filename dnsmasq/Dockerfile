FROM dadevel/c-builder:latest as dnsmasq
RUN apk add --no-cache gettext libidn2-dev libnetfilter_conntrack-dev linux-headers musl-libintl nettle-dev
COPY ./src/ ./config.patch .
RUN patch -u -i ./config.patch ./src/config.h && \
make -j $(nproc) all-i18n && \
strip ./src/dnsmasq

FROM dadevel/alpine:latest
# root must own ./data because dnsmasq accesses ./data/leases before switching user
RUN apk add --no-cache libidn2 libnetfilter_conntrack nettle && chown -R root:root ./data/
COPY --from=dnsmasq /build/src/dnsmasq ./bin/
COPY --from=dnsmasq /build/trust-anchors.conf ./static/
RUN dnsmasq --version
ENTRYPOINT ["dnsmasq", "--keep-in-foreground", "--user=app", "--group=app", "--pid-file=", "--log-facility=-", "--host-record=health.dnsmasq.test,127.0.0.1"]
HEALTHCHECK --interval=60s --timeout=3s --start-period=1s --retries=1 CMD ["nslookup", "health.dnsmasq.test", "127.0.0.1#53"]
EXPOSE 53/udp 67/udp 69/udp 547/udp

