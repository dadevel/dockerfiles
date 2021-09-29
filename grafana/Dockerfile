FROM --platform=$BUILDPLATFORM ghcr.io/dadevel/node:dev as grafana-web
COPY ./src .
RUN yarn install --pure-lockfile
ENV NODE_ENV=production
RUN yarn build

FROM ghcr.io/dadevel/go:dev as grafana
COPY ./src .
# grafana uses sqlite which requires cgo
ENV CGO_ENABLED=1
# TODO: investigate what linker option causes the trouble
ENV LDFLAGS="-Wl,-O1,-z,defs,-z,relro,-z,now,--hash-style=gnu,--no-copy-dt-needed-entries"
RUN go run ./build.go build-server
RUN mv ./bin/linux-*/grafana-server .
RUN strip ./grafana-server

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libssl1.1 && \
mkdir -p ./data/logs ./data/plugins ./config/provisioning/plugins ./config/provisioning/datasources ./config/provisioning/dashboards ./config/provisioning/notifiers && \
chown -R app:app ./data
COPY ./src/conf/defaults.ini ./static/conf/
COPY ./grafana.ini ./config/
COPY ./entrypoint.sh ./lib/
COPY --from=grafana-web /build/public ./static/public
COPY --from=grafana-web /build/tools ./static/tools
COPY --from=grafana /build/grafana-server ./bin/
RUN grafana-server -v
USER app
ENTRYPOINT ["./lib/entrypoint.sh", "--packaging", "docker", "--homepath", "./static", "--config", "./config/grafana.ini", "cfg:default.paths.data=/app/data", "cfg:default.paths.logs=/app/data/logs", "cfg:default.paths.plugins=/app/data/plugins", "cfg:default.paths.provisioning=/app/config/provisioning", "cfg:default.log.mode=console"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:3000/healthz"]
EXPOSE 3000/tcp
