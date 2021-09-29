FROM ghcr.io/dadevel/ubuntu:latest
RUN apt-get update && apt-get install --no-install-recommends -y perl libcapture-tiny-perl libconfig-inifiles-perl zfsutils-linux
COPY ./src/sanoid ./bin/
COPY ./src/sanoid.defaults.conf ./config/
COPY ./src/sanoid.conf ./config/
RUN sanoid --version
ENTRYPOINT ["sanoid", "--configdir", "./config"]
CMD ["--help"]
