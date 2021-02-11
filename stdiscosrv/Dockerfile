FROM ghcr.io/dadevel/go-builder:latest as stdiscosrv
COPY ./src .
RUN go run ./build.go -no-upgrade build stdiscosrv
RUN strip ./stdiscosrv
RUN ./stdiscosrv -version

FROM ghcr.io/dadevel/busybox:latest
COPY --from=stdiscosrv /build/stdiscosrv ./bin/
USER 1000:1000
ENTRYPOINT ["stdiscosrv", "-cert=./data/cert.pem", "-key=./data/key.pem", "-db-dir=./data/disco.db"]
CMD ["-listen=:8443", "-replication-listen=:19200", "-metrics-listen=:19201", "-http"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nc", "-z", "127.0.0.1", "8443"]
EXPOSE 8443/tcp 19200/tcp 19201/tcp

