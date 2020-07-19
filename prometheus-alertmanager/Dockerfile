FROM dadevel/go-builder:latest as alertmanager
RUN apk add --no-cache curl
COPY ./src/ .
RUN make -j $(nproc) common-build PROMU_BINARIES=alertmanager && \
strip ./alertmanager

FROM dadevel/distroless:latest
COPY --from=alertmanager /build/alertmanager ./bin/
RUN ["alertmanager", "--version"]
ENTRYPOINT ["alertmanager"]
CMD ["--config.file=/app/config/alertmanager.yaml", "--storage.path=/app/data"]
USER 1000:1000
EXPOSE 9093/tcp

