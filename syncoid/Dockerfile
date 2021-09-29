FROM ghcr.io/dadevel/ubuntu:latest
RUN apt-get install --no-install-recommends -y perl libcapture-tiny-perl lzop mbuffer zfsutils-linux
COPY ./src/syncoid ./bin/
RUN syncoid --version
ENTRYPOINT ["syncoid"]
CMD ["--help"]
