FROM node:12-alpine as webui
WORKDIR /build/src/
COPY ./src/webui/ .
RUN npm install
RUN npm run build

FROM dadevel/go-builder:latest as traefik
RUN apk add --no-cache bash
RUN go get -u github.com/containous/go-bindata/...
WORKDIR /go/src/github.com/containous/traefik/
COPY ./src/ .
COPY --from=webui /build/static/ ./static/
RUN go generate && \
go build ./cmd/traefik && \
strip ./traefik && \
setcap -q cap_net_bind_service+ep ./traefik && \
mv ./traefik /build/

FROM dadevel/distroless:latest
COPY --from=traefik /build/traefik /app/bin/
RUN ["traefik", "version"]
ENTRYPOINT ["traefik"]
CMD ["--configfile", "/app/config/traefik.yaml"]
HEALTHCHECK --interval=60s --timeout=3s --start-period=1s --retries=1 CMD ["traefik", "healthcheck", "--configfile", "/app/config/traefik.yaml"]

