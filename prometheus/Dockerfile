FROM --platform=$BUILDPLATFORM ghcr.io/dadevel/node:dev as prometheus-web
COPY ./src/web/ui/react-app .
ENV PUBLIC_URL=.
# part one of 'assets' target from makefile
RUN yarn install --frozen-lockfile
RUN yarn build

FROM ghcr.io/dadevel/go:dev as prometheus
ENV GO111MODULE=on
COPY ./src .
COPY --from=prometheus-web /build/build ./web/ui/static/react
# part two of 'assets' target from makefile
RUN cd ./web/ui && go generate -x -v
# build binary
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
