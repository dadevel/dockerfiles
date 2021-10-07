FROM ghcr.io/dadevel/go:dev as node-exporter
COPY ./src .
RUN make -j $(nproc) common-build
RUN mv ./node_exporter ./node-exporter
RUN strip ./node-exporter

FROM ghcr.io/dadevel/debian:latest
COPY --from=node-exporter /build/node-exporter ./bin/
RUN node-exporter --version
USER app
ENTRYPOINT ["node-exporter", "--collector.textfile.directory=./textfiles", "--path.rootfs=/rootfs"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9100/health"]
EXPOSE 9100/tcp
VOLUME /app/config /app/textfiles
