FROM ghcr.io/dadevel/go:dev as lego
ENV GO111MODULE=on
COPY ./src .
RUN make build
RUN strip ./dist/lego

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y openssl
COPY ./entrypoint.sh ./lib/
COPY --from=lego /build/dist/lego ./bin/
RUN lego --version
USER app
ENTRYPOINT ["./lib/entrypoint.sh"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["ls", "-d", "/dev/shm/healthy"]
VOLUME /app/certs
