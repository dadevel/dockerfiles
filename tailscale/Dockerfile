FROM docker.io/library/golang:alpine AS authkey
RUN go install tailscale.com/cmd/get-authkey@latest

FROM docker.io/library/alpine:latest
RUN apk add --no-cache tailscale socat
COPY --from=authkey /go/bin/get-authkey /usr/local/bin/get-authkey
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
VOLUME /var/lib/tailscale
EXPOSE 8080/tcp
