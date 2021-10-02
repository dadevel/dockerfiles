FROM ghcr.io/dadevel/debian:latest
# install podman from https://build.opensuse.org/package/show/devel:kubic:libcontainers:stable/podman
RUN wget -q -O /etc/apt/trusted.gpg.d/kubic.asc https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/Debian_11/Release.key
COPY ./kubic.list /etc/apt/sources.list.d/
RUN apt-get update && apt-get install --no-install-recommends -y podman
COPY ./entrypoint.sh ./lib/
ENV XDG_RUNTIME_DIR=/run
ENTRYPOINT ["./lib/entrypoint.sh"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["ls", "-d", "/dev/shm/healthy"]
