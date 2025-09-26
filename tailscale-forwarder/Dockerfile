FROM docker.io/tailscale/tailscale:latest
RUN apk add --no-cache socat && mkdir /var/lib/tailscale && chown -R nobody:nobody /var/lib/tailscale
COPY ./entrypoint.sh /
USER nobody
ENTRYPOINT ["/entrypoint.sh"]
CMD []
EXPOSE 1080/tcp 8080/tcp
VOLUME /var/lib/tailscale
