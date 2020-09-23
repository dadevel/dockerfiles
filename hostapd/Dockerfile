FROM dadevel/c-builder:latest as hostapd
RUN apk add --no-cache libnl3-dev linux-headers openssl-dev
COPY ./src/ .
COPY ./src/hostapd/defconfig ./hostapd/.config
COPY ./config.patch ./hostapd/
RUN cd ./hostapd && patch -u -i ./config.patch ./.config && make -j $(nproc) && strip ./hostapd

FROM dadevel/alpine:latest
ARG TARGETARCH
RUN apk add --no-cache iw libnl3 openssl && \
[ $TARGETARCH != arm ] || apk add --no-cache libgcc
COPY ./entrypoint.sh ./bin/
COPY --from=hostapd /build/hostapd/hostapd ./bin/
# hostapd -v always exits with return code 1
RUN hostapd -v || [ $? -eq 1 ]
ENTRYPOINT ["entrypoint.sh", "-P", "/dev/shm/hostapd.pid", "-g", "/dev/shm/hostapd", "-G", "app"]

