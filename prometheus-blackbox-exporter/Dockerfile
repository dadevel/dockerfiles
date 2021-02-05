FROM dadevel/go-builder:latest as blackbox-exporter
RUN apk add --no-cache curl
COPY ./src .
RUN make -j $(nproc) common-build
RUN mv ./blackbox_exporter ./blackbox-exporter
RUN strip ./blackbox-exporter
RUN ./blackbox-exporter --version

FROM dadevel/busybox:latest
COPY --from=blackbox-exporter /build/blackbox-exporter ./bin/
COPY ./blackbox-exporter.yaml ./config/
USER 1000
ENTRYPOINT ["blackbox-exporter", "--config.file=./config/blackbox-exporter.yaml"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:9115/"]
EXPOSE 9115/tcp

