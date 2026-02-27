FROM docker.io/library/alpine:latest AS src
WORKDIR /build
RUN apk add --no-cache git
RUN git clone https://github.com/zrepl/zrepl.git . && \
git checkout "$(git tag | grep '^v' | sort -Vu | tail -n1)"

FROM docker.io/library/golang:alpine AS zrepl
WORKDIR /build
RUN apk add --no-cache binutils gawk make unzip
ENV ZREPL_VERSION=latest
COPY --from=src /build/ .
RUN make -j $(nproc) zrepl-bin
RUN ls -la ./artifacts/zrepl-*
RUN mv ./artifacts/zrepl-* ./zrepl && strip ./zrepl

FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache zfs
COPY --from=zrepl /build/zrepl /app/bin/
RUN zrepl help
ENTRYPOINT ["zrepl", "daemon"]
CMD ["--config", "/app/config/zrepl.yaml"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["zrepl", "version"]
EXPOSE 8888/tcp 9811/tcp
VOLUME /app/config

