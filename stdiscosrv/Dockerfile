FROM dadevel/go-builder:latest as stdiscosrv
COPY ./src/ .
RUN go run ./build.go -no-upgrade build stdiscosrv && strip ./stdiscosrv

FROM dadevel/distroless:latest
COPY --from=stdiscosrv /build/stdiscosrv ./bin/
USER 1000:1000
RUN ["stdiscosrv", "-version"]
ENTRYPOINT ["stdiscosrv", "-cert=./config/cert.pem", "-key=./config/key.pem", "-db-dir=./data/disco.db"]
CMD ["-listen=:8443", "-replication-listen=:19200", "-metrics-listen=:19201", "-http"]
EXPOSE 8443/tcp 19200/tcp 19201/tcp

