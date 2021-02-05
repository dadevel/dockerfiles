FROM dadevel/go-builder:latest as node-exporter
RUN apk add --no-cache curl
COPY ./src .
RUN make -j $(nproc) common-build
RUN mv ./node_exporter ./node-exporter
RUN strip ./node-exporter
RUN ./node-exporter --version

FROM dadevel/busybox:latest
COPY --from=node-exporter /build/node-exporter ./bin/
USER 1000
ENTRYPOINT ["node-exporter", "--collector.textfile.directory=./cache", "--path.rootfs=/rootfs"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:9100/health"]
EXPOSE 9100/tcp

