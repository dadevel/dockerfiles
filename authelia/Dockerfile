FROM --platform=$BUILDPLATFORM ghcr.io/dadevel/node:dev as authelia-web
COPY ./src/web .
RUN yarn install --frozen-lockfile
ENV NODE_ENV=production
RUN yarn build

FROM ghcr.io/dadevel/go:dev as authelia
COPY ./src .
# authelia uses sqlite which requires cgo
ENV CGO_ENABLED=1
COPY --from=authelia-web /internal/server/public_html ./internal/server/public_html
RUN mv ./api ./internal/server/public_html/api
RUN go build -ldflags '-linkmode=external -s -w' -trimpath -buildmode=pie -o ./authelia ./cmd/authelia
RUN strip ./authelia

FROM ghcr.io/dadevel/debian:latest
COPY --from=authelia /build/authelia ./bin/authelia
RUN authelia --version
USER app
ENTRYPOINT ["authelia", "--config", "./config/authelia.yaml"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:9091/api/health"]
EXPOSE 9091/tcp
VOLUME /app/config /app/data
