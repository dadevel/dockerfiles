FROM dadevel/c-builder:latest as hostapd
RUN apk add --no-cache libnl3-dev linux-headers openssl-dev
COPY ./src/ .
COPY ./src/hostapd/defconfig ./hostapd/.config
COPY ./config.patch ./hostapd/
RUN cd ./hostapd && patch -u -i ./config.patch ./.config && make -j $(nproc) && strip ./hostapd

FROM dadevel/alpine:latest
COPY --from=hostapd /build/hostapd/hostapd /app/bin/
RUN apk add --no-cache libnl3 openssl
# hostapd -v always exits with return code 1
RUN hostapd -v || [ $? -eq 1 ]
ENTRYPOINT ["hostapd"]
CMD ["-P", "/dev/shm/hostapd.pid", "-g", "/dev/shm/hostapd", "-G", "app", "/app/config/hostapd.conf"]

