FROM node:12-alpine as webui
WORKDIR /build
COPY ./src/ .
RUN yarn install --pure-lockfile --no-progress
ENV NODE_ENV production
RUN ./node_modules/.bin/grunt build

FROM dadevel/go-builder:latest as grafana
ARG TARGETARCH=amd64
COPY ./src/ .
# grafana uses sqlite which requires cgo
ENV CGO_ENABLED 1
ENV LDFLAGS ""
RUN echo "LDFLAGS=$LDFLAGS;"
RUN unset LDFLAGS && \
go run ./build.go build-server && \
strip ./bin/linux-$TARGETARCH/grafana-server

FROM dadevel/alpine:latest
ARG TARGETARCH=amd64
RUN apk add --no-cache musl-utils openssl
RUN mkdir -p ./data/plugins \
./config/provisioning/datasources \
./config/provisioning/dashboards \
./config/provisioning/notifiers && \
chown -R app:app ./data/plugins
COPY ./src/conf/defaults.ini ./static/conf/
COPY --from=webui /build/public ./static/public
COPY --from=webui /build/tools ./static/tools
COPY --from=grafana /build/bin/linux-$TARGETARCH/grafana-server ./bin/
RUN grafana-server -v
ENTRYPOINT ["grafana-server", "--packaging=docker", "--homepath=/app/static", "--config=/app/config/grafana.ini", "cfg:default.paths.data=/app/data", "cfg:default.paths.plugins=/app/data/plugins", "cfg:default.paths.provisioning=/app/config/provisioning", "cfg:default.log.mode=console"]
USER 1000:1000
EXPOSE 3000/tcp

