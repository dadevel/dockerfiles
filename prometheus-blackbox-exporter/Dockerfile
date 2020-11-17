FROM dadevel/go-builder:latest as blackbox-exporter
RUN apk add --no-cache curl
COPY ./src/ .
RUN make -j $(nproc) common-build && mv ./build ./blackbox-exporter && strip ./blackbox-exporter

FROM dadevel/busybox:latest
COPY --from=blackbox-exporter /build/blackbox-exporter ./bin/
USER 1000
RUN ["blackbox-exporter", "--version"]
ENTRYPOINT ["blackbox-exporter", "--config.file=./config/blackbox-exporter.yaml"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "http://127.0.0.1:9115/health"]
EXPOSE 9115/tcp

