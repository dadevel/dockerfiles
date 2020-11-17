FROM dadevel/c-builder:latest as hostapd
RUN apk add --no-cache linux-headers libnl3-dev libressl-dev
COPY ./src/ .
COPY ./config.txt ./hostapd/.config
RUN cd ./hostapd/ && \
make -j $(nproc) && \
strip ./hostapd && \
strip ./hostapd_cli

FROM dadevel/alpine:latest
ARG TARGETARCH
RUN apk add --no-cache iw libnl3 libressl && \
[ $TARGETARCH != arm ] || apk add --no-cache libgcc
COPY ./entrypoint.sh ./lib/
COPY --from=hostapd /build/hostapd/hostapd ./bin/
COPY --from=hostapd /build/hostapd/hostapd_cli ./bin/
# hostapd -v always exits with return code 1
RUN hostapd -v || [ $? -eq 1 ]
ENTRYPOINT ["./lib/entrypoint.sh", "-P", "/dev/shm/hostapd.pid", "-g", "/dev/shm/hostapd", "-G", "app"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["hostapd_cli", "quit"]

