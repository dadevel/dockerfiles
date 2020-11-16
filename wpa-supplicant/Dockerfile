FROM dadevel/c-builder:latest as wpa-supplicant
RUN apk add --no-cache linux-headers libnl3-dev openssl-dev dbus-dev pcsc-lite-dev
COPY ./src/ .
COPY ./config.txt ./wpa_supplicant/.config
RUN cd ./wpa_supplicant/ && \
make -j $(nproc) && \
strip ./wpa_supplicant && \
strip ./wpa_cli && \
strip ./wpa_passphrase

FROM dadevel/alpine:latest
ARG TARGETARCH
RUN apk add --no-cache libnl3 openssl dbus-libs pcsc-lite-libs && \
[ $TARGETARCH != arm ] || apk add --no-cache libgcc
COPY --from=wpa-supplicant /build/wpa_supplicant/wpa_supplicant ./bin/
COPY --from=wpa-supplicant /build/wpa_supplicant/wpa_cli ./bin/
COPY --from=wpa-supplicant /build/wpa_supplicant/wpa_passphrase ./bin/
RUN wpa_supplicant -v
ENTRYPOINT ["wpa_supplicant", "-P", "/dev/shm/wpa_supplicant.pid"]
CMD ["-c", "./config/wpa_supplicant.conf"]

