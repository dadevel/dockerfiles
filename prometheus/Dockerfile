FROM --platform=$BUILDPLATFORM ghcr.io/dadevel/node:dev AS prometheus-web
COPY ./src .
# parallelization breaks the build
RUN make assets-compress

FROM ghcr.io/dadevel/go:dev AS prometheus
ENV GO111MODULE=on
COPY ./src .
COPY --from=prometheus-web /build/web/ui/ ./web/ui/
RUN make -j $(nproc) common-build PROMU_BINARIES=prometheus
RUN strip ./prometheus

FROM ghcr.io/dadevel/debian:latest
COPY ./prometheus.yaml ./config/
COPY --from=prometheus /build/prometheus ./bin/
RUN prometheus --version
USER app
ENTRYPOINT ["prometheus", "--config.file=./config/prometheus.yaml", "--storage.tsdb.path=./data", "--web.console.libraries=./config/console_libraries", "--web.console.templates=./config/consoles"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9090/-/healthy"]
EXPOSE 9090/tcp
VOLUME /app/config /app/data
