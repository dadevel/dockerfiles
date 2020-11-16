FROM dadevel/go-builder:latest as node-exporter
RUN apk add --no-cache curl
COPY ./src/ .
RUN make -j $(nproc) common-build && strip ./node_exporter

FROM dadevel/distroless:latest
COPY --from=node-exporter /build/node_exporter ./bin/node-exporter
USER 1000
RUN ["node-exporter", "--version"]
ENTRYPOINT ["node-exporter", "--collector.textfile.directory=./data", "--path.rootfs=/rootfs"]
EXPOSE 9100/tcp

