FROM ghcr.io/dadevel/ubuntu-focal:latest
COPY ./src/sanoid ./bin/
COPY ./src/sanoid.defaults.conf ./config/
COPY ./src/sanoid.conf ./config/
RUN apt-get update && apt-get install --no-install-recommends --yes perl libcapture-tiny-perl libconfig-inifiles-perl zfsutils-linux
RUN sanoid --version
ENTRYPOINT ["sanoid", "--configdir", "./config"]
CMD ["--help"]

