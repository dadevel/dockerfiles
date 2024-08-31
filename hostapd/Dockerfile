FROM ghcr.io/dadevel/cxx:dev AS hostapd
RUN apt-get update && apt-get install --no-install-recommends -y linux-headers-generic libnl-3-dev libnl-genl-3-dev libnl-route-3-dev libssl-dev pkg-config
COPY ./src .
COPY ./config.txt ./hostapd/.config
RUN cd ./hostapd && make -j $(nproc)
RUN strip ./hostapd/hostapd ./hostapd/hostapd_cli

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y iw libnl-3-200 libnl-genl-3-200 libnl-route-3-200 libssl3
COPY ./entrypoint.sh ./lib/
COPY ./hostapd.conf ./config/
COPY --from=hostapd /build/hostapd/hostapd ./bin/
COPY --from=hostapd /build/hostapd/hostapd_cli ./bin/
RUN hostapd -v || [ $? -eq 1 ]
ENTRYPOINT ["./lib/entrypoint.sh", "-P", "/dev/shm/hostapd.pid", "-g", "/dev/shm/hostapd", "-G", "root"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["hostapd_cli", "-p", "/dev/shm/hostapd", "quit"]
VOLUME /app/config
