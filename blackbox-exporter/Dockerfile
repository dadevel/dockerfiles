FROM ghcr.io/dadevel/go:dev as blackbox-exporter
COPY ./src .
RUN make -j $(nproc) common-build
RUN mv ./blackbox_exporter ./blackbox-exporter
RUN strip ./blackbox-exporter

FROM ghcr.io/dadevel/debian:latest
COPY ./blackbox-exporter.yaml ./config/
COPY --from=blackbox-exporter /build/blackbox-exporter ./bin/
RUN blackbox-exporter --version
USER app
ENTRYPOINT ["blackbox-exporter", "--config.file=./config/blackbox-exporter.yaml"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9115/"]
EXPOSE 9115/tcp
VOLUME /app/config
