FROM dadevel/go-builder:latest as blackbox-exporter
RUN apk add --no-cache curl
COPY ./src/ .
RUN make -j $(nproc) common-build && mv ./build ./blackbox-exporter && strip ./blackbox-exporter

FROM dadevel/distroless:latest
COPY --from=blackbox-exporter /build/blackbox-exporter ./bin/
USER 1000
RUN ["blackbox-exporter", "--version"]
ENTRYPOINT ["blackbox-exporter", "--config.file=./config/blackbox-exporter.yaml"]
EXPOSE 9115/tcp

