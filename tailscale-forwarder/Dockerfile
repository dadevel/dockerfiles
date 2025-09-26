FROM docker.io/tailscale/tailscale:latest
RUN apk add --no-cache socat && mkdir /home/tailscale
COPY ./entrypoint.sh /
USER root
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 1080/tcp 8080/tcp
VOLUME /home/tailscale
