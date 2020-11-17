FROM dadevel/go-builder:latest as cadvisor
COPY ./src/ .
RUN cd ./cmd/ && go build . && strip ./cmd && mv ./cmd /build/cadvisor

FROM dadevel/busybox:latest
COPY --from=cadvisor /build/cadvisor ./bin/
RUN ["cadvisor", "-version"]
ENTRYPOINT ["cadvisor", "-logtostderr"]
CMD ["-port", "9338"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:9338/healthz"]

