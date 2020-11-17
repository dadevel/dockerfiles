FROM dadevel/go-builder:latest as prometheus
RUN apk add --no-cache bash curl yarn
COPY ./src/ .
RUN make -j $(nproc) assets && \
make -j $(nproc) common-build PROMU_BINARIES=prometheus && \
strip ./prometheus

FROM dadevel/busybox:latest
COPY --from=prometheus /build/prometheus ./bin/
USER 1000
RUN ["prometheus", "--version"]
ENTRYPOINT ["prometheus", "--config.file=./config/prometheus.yaml", "--storage.tsdb.path=./data", "--web.console.libraries=./config/console_libraries", "--web.console.templates=./config/consoles"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "http://127.0.0.1:9090/-/healthy"]
EXPOSE 9090/tcp

