FROM --platform=$BUILDPLATFORM node:12-alpine as prometheus-web
WORKDIR /build
COPY ./src/web/ui/react-app .
ENV PUBLIC_URL .
# part one of 'assets' target from makefile
RUN yarn install --frozen-lockfile
RUN yarn build

FROM ghcr.io/dadevel/go-builder:latest as prometheus
ENV GO111MODULE on
RUN apk add --no-cache curl
COPY ./src .
COPY --from=prometheus-web /build/build ./web/ui/static/react
# part two of 'assets' target from makefile
RUN cd ./web/ui && go generate -x -v -mod=vendor
# build binary
RUN make -j $(nproc) common-build PROMU_BINARIES=prometheus
RUN strip ./prometheus
RUN ./prometheus --version

FROM ghcr.io/dadevel/busybox:latest
COPY --from=prometheus /build/prometheus ./bin/
COPY ./prometheus.yaml ./config/
USER 1000
ENTRYPOINT ["prometheus", "--config.file=./config/prometheus.yaml", "--storage.tsdb.path=./data", "--web.console.libraries=./config/console_libraries", "--web.console.templates=./config/consoles"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:9090/-/healthy"]
EXPOSE 9090/tcp

