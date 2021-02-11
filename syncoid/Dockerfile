FROM ghcr.io/dadevel/ubuntu-focal:latest
RUN apt-get update && apt-get install --no-install-recommends --yes perl libcapture-tiny-perl lzop mbuffer zfsutils-linux
COPY ./src/syncoid ./bin/
RUN syncoid --version
ENTRYPOINT ["syncoid"]
CMD ["--help"]

