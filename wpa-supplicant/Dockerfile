FROM ghcr.io/dadevel/cxx-builder:latest as wpa-supplicant
RUN apk add --no-cache linux-headers libnl3-dev libressl-dev dbus-dev pcsc-lite-dev
COPY ./src .
COPY ./config.txt ./wpa_supplicant/.config
RUN cd ./wpa_supplicant && make -j $(nproc)
RUN strip ./wpa_supplicant/wpa_supplicant ./wpa_supplicant/wpa_cli ./wpa_supplicant/wpa_passphrase
RUN ./wpa_supplicant/wpa_supplicant -v

FROM ghcr.io/dadevel/alpine:latest
ARG TARGETARCH
RUN apk add --no-cache libnl3 libressl dbus-libs pcsc-lite-libs && \
[ $TARGETARCH != arm ] || apk add --no-cache libgcc
COPY --from=wpa-supplicant /build/wpa_supplicant/wpa_supplicant /build/wpa_supplicant/wpa_cli /build/wpa_supplicant/wpa_passphrase ./bin/
ENTRYPOINT ["wpa_supplicant", "-P", "/dev/shm/wpa_supplicant.pid", "-c", "./config/wpa_supplicant.conf"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wpa_cli", "-p", "/dev/shm/wpa-supplicant", "quit"]

