FROM ghcr.io/dadevel/go:dev AS stdiscosrv
COPY ./src .
RUN go run ./build.go -no-upgrade build stdiscosrv
RUN strip ./stdiscosrv

FROM ghcr.io/dadevel/debian:latest
COPY --from=stdiscosrv /build/stdiscosrv ./bin/
RUN stdiscosrv -version
USER app
ENTRYPOINT ["stdiscosrv", "-cert=./data/cert.pem", "-key=./data/key.pem", "-db-dir=./data/disco.db"]
CMD ["-listen=:8443", "-replication-listen=:19200", "-metrics-listen=:19201", "-http"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nc", "-z", "localhost", "8443"]
EXPOSE 8443/tcp 19200/tcp 19201/tcp
VOLUME /app/data
