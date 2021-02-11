FROM ghcr.io/dadevel/go-builder:latest as strelaysrv
COPY ./src .
RUN go run ./build.go -no-upgrade build strelaysrv
RUN strip ./strelaysrv
RUN ./strelaysrv -version

FROM ghcr.io/dadevel/busybox:latest
COPY --from=strelaysrv /build/strelaysrv ./bin/
USER 1000:1000
ENTRYPOINT ["strelaysrv", "-keys=./data"]
CMD ["-listen=:22067", "-status-srv=:22070", "-pools="]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nc", "-z", "127.0.0.1", "22067"]
EXPOSE 22067/tcp 22070/tcp

