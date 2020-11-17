ARG BUILDPLATFORM
FROM --platform=$BUILDPLATFORM node:12-alpine as webui
WORKDIR /build
COPY ./src/ .
RUN yarn install --pure-lockfile --no-progress
ENV NODE_ENV production
RUN ./node_modules/.bin/grunt build

FROM dadevel/go-builder:latest as grafana
COPY ./src/ .
# grafana uses sqlite which requires cgo
ENV CGO_ENABLED 1
ENV LDFLAGS ""
RUN go run ./build.go build-server && \
mv ./bin/linux-*/grafana-server . && \
strip ./grafana-server

FROM dadevel/alpine:latest
RUN apk add --no-cache musl-utils libressl && \
mkdir -p \
./data/log/ \
./data/plugins/ \
./config/provisioning/plugins \
./config/provisioning/datasources \
./config/provisioning/dashboards \
./config/provisioning/notifiers && \
chown -R app:app ./data/
COPY ./src/conf/defaults.ini ./static/conf/
COPY ./entrypoint.sh ./lib/
COPY --from=webui /build/public ./static/public
COPY --from=webui /build/tools ./static/tools
COPY --from=grafana /build/grafana-server ./bin/
USER app
RUN grafana-server -v
ENTRYPOINT ["./lib/entrypoint.sh", "--packaging", "docker", "--homepath", "./static", "--config", "./config/grafana.ini", "cfg:default.paths.data=./data", "cfg:default.paths.logs=./data/log", "cfg:default.paths.plugins=./data/plugins", "cfg:default.paths.provisioning=./config/provisioning", "cfg:default.log.mode=console"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:3000/healthz"]
EXPOSE 3000/tcp

