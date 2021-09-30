FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y inotify-tools jq
COPY ./entrypoint.sh ./lib/
USER app
ENTRYPOINT ["./lib/entrypoint.sh"]
