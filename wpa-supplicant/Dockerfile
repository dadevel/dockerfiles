FROM ghcr.io/dadevel/cxx:dev as wpa-supplicant
RUN apt-get update && apt-get install --no-install-recommends -y linux-headers-generic libnl-3-dev libnl-genl-3-dev libnl-route-3-dev libssl-dev libdbus-1-dev libdbus-glib-1-dev libpcsclite-dev
COPY ./src .
COPY ./config.txt ./wpa_supplicant/.config
RUN cd ./wpa_supplicant && make -j $(nproc)
RUN strip ./wpa_supplicant/wpa_supplicant ./wpa_supplicant/wpa_cli ./wpa_supplicant/wpa_passphrase

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libnl-3-200 libnl-genl-3-200 libnl-route-3-200 libssl3 libdbus-1-3 libdbus-glib-1-2 libpcsclite1
COPY --from=wpa-supplicant /build/wpa_supplicant/wpa_supplicant /build/wpa_supplicant/wpa_cli /build/wpa_supplicant/wpa_passphrase ./bin/
RUN wpa_supplicant -v
ENTRYPOINT ["wpa_supplicant", "-P", "/dev/shm/wpa_supplicant.pid", "-c", "./config/wpa_supplicant.conf"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wpa_cli", "-p", "/dev/shm/wpa-supplicant", "quit"]
VOLUME /app/config
