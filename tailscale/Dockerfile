FROM docker.io/library/alpine:latest
RUN apk add --no-cache tailscale socat
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
VOLUME /var/lib/tailscale
EXPOSE 8080/tcp
