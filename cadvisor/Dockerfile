FROM ghcr.io/dadevel/go:dev as cadvisor
COPY ./src .
RUN cd ./cmd && go build . && mv ./cmd ../cadvisor
RUN strip ./cadvisor

FROM ghcr.io/dadevel/debian:latest
COPY --from=cadvisor /build/cadvisor ./bin/
RUN cadvisor -version
ENTRYPOINT ["cadvisor", "-logtostderr"]
CMD ["-port", "9338"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9338/healthz"]
EXPOSE 9338/tcp
