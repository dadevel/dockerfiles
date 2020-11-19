FROM dadevel/go-builder:latest as alertmanager
RUN apk add --no-cache curl
COPY ./src .
RUN make -j $(nproc) common-build PROMU_BINARIES=alertmanager
RUN strip ./alertmanager
RUN ./alertmanager --version

FROM dadevel/busybox:latest
COPY --from=alertmanager /build/alertmanager ./bin/
COPY ./alertmanager.yaml ./config/
USER 1000
ENTRYPOINT ["alertmanager", "--config.file=./config/alertmanager.yaml", "--storage.path=./data"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:9093/-/healthy"]
EXPOSE 9093/tcp

