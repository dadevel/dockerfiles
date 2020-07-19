FROM dadevel/go-builder:latest as prometheus
RUN apk add --no-cache bash curl yarn
COPY ./src/ .
RUN make -j $(nproc) assets && \
make -j $(nproc) common-build PROMU_BINARIES=prometheus && \
strip ./prometheus

FROM dadevel/distroless:latest
COPY --from=prometheus /build/prometheus ./bin/
RUN ["prometheus", "--version"]
ENTRYPOINT ["prometheus"]
CMD ["--config.file=/app/config/prometheus.yaml", "--storage.tsdb.path=/app/data", "--web.console.libraries=/app/config/console_libraries", "--web.console.templates=/app/config/consoles"]
USER 1000:1000
EXPOSE 9090/tcp

