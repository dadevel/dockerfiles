FROM docker.io/tailscale/tailscale:latest
RUN apk add --no-cache socat
COPY ./entrypoint.sh /
USER nobody
ENTRYPOINT ["/entrypoint.sh"]
CMD []
EXPOSE 1080/tcp 8080/tcp
VOLUME /var/lib/tailscale
