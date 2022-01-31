FROM ghcr.io/dadevel/go:dev as zrepl
COPY ./src .
RUN apt-get update && apt-get install --no-install-recommends -y gawk unzip
RUN bash ./build.installprotoc.bash
RUN bash ./lazy.sh godep
# patch default paths
RUN sed -i 's|/etc/zrepl|/app/config|g;s|/var/run/zrepl|/dev/shm/zrepl|g;' **/*.go
RUN make -j $(nproc) zrepl-bin
RUN mv ./artifacts/zrepl-linux-* ./zrepl
RUN strip ./zrepl

FROM ghcr.io/dadevel/ubuntu:latest
RUN apt-get update && apt-get install --no-install-recommends -y zfsutils-linux
COPY ./entrypoint.sh ./lib/
COPY --from=zrepl /build/zrepl ./bin/
RUN zrepl help
ENTRYPOINT ["./lib/entrypoint.sh"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["zrepl", "version"]
EXPOSE 8888/tcp 9811/tcp
VOLUME /app/config
