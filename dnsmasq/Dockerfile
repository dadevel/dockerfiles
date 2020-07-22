FROM dadevel/c-builder:latest as dnsmasq
RUN apk add --no-cache gettext libidn2-dev libnetfilter_conntrack-dev linux-headers musl-libintl nettle-dev
COPY ./src .
COPY ./config.patch .
RUN patch -u -i ./config.patch ./src/config.h && \
rm ./config.patch && \
make -j $(nproc) all-i18n && \
strip ./src/dnsmasq

FROM dadevel/alpine:latest
COPY --from=dnsmasq /build/src/dnsmasq ./bin/
COPY --from=dnsmasq /build/trust-anchors.conf ./static/
RUN apk add --no-cache libidn2 libnetfilter_conntrack nettle && dnsmasq --version
# dnsmasq accesses ./data before dropping privileges
RUN chown -R root:root ./data/
ENTRYPOINT ["dnsmasq", "--keep-in-foreground", "--user=app", "--group=app", "--pid-file=", "--log-facility=-", "--host-record=health.dnsmasq.test,127.0.0.1"]
HEALTHCHECK --interval=60s --timeout=3s --start-period=1s --retries=1 CMD ["nslookup", "health.dnsmasq.test", "127.0.0.1#53"]
EXPOSE 53/udp 67/udp 69/udp 547/udp

