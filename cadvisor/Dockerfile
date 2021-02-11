FROM ghcr.io/dadevel/go-builder:latest as cadvisor
COPY ./src .
RUN cd ./cmd && go build . && mv ./cmd /build/cadvisor
RUN strip ./cadvisor
RUN ./cadvisor -version

FROM ghcr.io/dadevel/busybox:latest
COPY --from=cadvisor /build/cadvisor ./bin/
ENTRYPOINT ["cadvisor", "-logtostderr"]
CMD ["-port", "9338"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:9338/healthz"]
EXPOSE 9338/tcp

