FROM node:12-alpine as webui
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
RUN apk add --no-cache musl-utils openssl
RUN mkdir -p ./data/log/ ./data/plugins/ \
./config/provisioning/plugins \
./config/provisioning/datasources \
./config/provisioning/dashboards \
./config/provisioning/notifiers && \
chown -R app:app ./data/
COPY ./src/conf/defaults.ini ./static/conf/
COPY ./entrypoint.sh ./bin/
COPY --from=webui /build/public ./static/public
COPY --from=webui /build/tools ./static/tools
COPY --from=grafana /build/grafana-server ./bin/
RUN grafana-server -v
ENTRYPOINT ["entrypoint.sh", "--packaging", "docker", "--homepath", "/app/static", "--config", "/app/config/grafana.ini", "cfg:default.paths.data=/app/data", "cfg:default.paths.logs=/app/data/log", "cfg:default.paths.plugins=/app/data/plugins", "cfg:default.paths.provisioning=/app/config/provisioning", "cfg:default.log.mode=console"]
USER app
EXPOSE 3000/tcp

