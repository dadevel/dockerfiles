FROM ghcr.io/dadevel/go:dev as fritzbox-exporter
ENV GO111MODULE=off
COPY ./src/ /go/src/github.com/sberk42/fritzbox_exporter/
WORKDIR /go/src/github.com/sberk42/fritzbox_exporter/
RUN go get .
RUN go build .
RUN strip ./fritzbox_exporter
RUN mv ./fritzbox_exporter /build/

FROM ghcr.io/dadevel/debian:latest
COPY ./entrypoint.sh ./lib/
COPY ./src/metrics.json ./src/metrics-lua.json ./static/
COPY --from=fritzbox-exporter /build/fritzbox_exporter ./bin/fritzbox-exporter
RUN fritzbox-exporter -h || [ $? -eq 2 ]
USER app
ENTRYPOINT ["./lib/entrypoint.sh"]
CMD ["-listen-address", ":9042", "-metrics-file", "./static/metrics.json", "-lua-metrics-file", "./static/metrics-lua.json"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nc", "-z", "localhost", "9042"]
EXPOSE 9042/tcp
