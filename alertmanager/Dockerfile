FROM ghcr.io/dadevel/go:dev AS alertmanager
COPY ./src .
RUN make -j $(nproc) common-build PROMU_BINARIES=alertmanager
RUN strip ./alertmanager

FROM ghcr.io/dadevel/debian:latest
COPY ./alertmanager.yaml ./config/
COPY --from=alertmanager /build/alertmanager ./bin/
RUN alertmanager --version
USER app
ENTRYPOINT ["alertmanager", "--config.file=./config/alertmanager.yaml", "--storage.path=./data"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9093/-/healthy"]
EXPOSE 9093/tcp
VOLUME /app/config /app/data
