FROM ghcr.io/dadevel/go:dev AS strelaysrv
COPY ./src .
RUN go run ./build.go -no-upgrade build strelaysrv
RUN strip ./strelaysrv

FROM ghcr.io/dadevel/debian:latest
COPY --from=strelaysrv /build/strelaysrv ./bin/
RUN strelaysrv -version
USER app
ENTRYPOINT ["strelaysrv", "-keys=./data"]
CMD ["-listen=:22067", "-status-srv=:22070", "-pools="]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nc", "-z", "localhost", "22067"]
EXPOSE 22067/tcp 22070/tcp
VOLUME /app/data
