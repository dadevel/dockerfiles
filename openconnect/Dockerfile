FROM ghcr.io/dadevel/cxx:dev as openconnect
# see https://www.infradead.org/openconnect/building.html
RUN apt-get update && apt-get install --no-install-recommends -y automake libtool pkg-config libxml2-dev zlib1g-dev libssl-dev liblz4-dev libpskc-dev
COPY ./src .
RUN curl -o ./vpnc-script https://gitlab.com/openconnect/vpnc-scripts/raw/master/vpnc-script && \
chmod 0755 ./vpnc-script
# without -pie
ENV LDFLAGS="-Wl,-O1,-z,defs,-z,relro,-z,now,--hash-style=gnu,--no-copy-dt-needed-entries"
RUN ./autogen.sh
RUN ./configure --prefix=/app --with-vpnc-script=/app/lib/vpnc-script --with-pic --disable-nls --disable-static
RUN make -j $(nproc)
RUN strip ./.libs/openconnect
RUN make install

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libxml2 libpskc0 python3 python3-asn1crypto python3-mechanize python3-netifaces iproute2 systemd libnss-resolve
COPY ./entrypoint.sh /
COPY --from=openconnect /app/sbin/ /app/bin/
COPY --from=openconnect /app/lib/ /app/lib/
COPY --from=openconnect /build/trojans/tncc-emulate.py ./lib/
COPY --from=openconnect /build/vpnc-script ./lib/
RUN openconnect --version
ENTRYPOINT ["/entrypoint.sh"]
