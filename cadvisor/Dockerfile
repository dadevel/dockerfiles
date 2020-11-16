FROM dadevel/go-builder:latest as cadvisor
COPY ./src/ .
RUN cd ./cmd/ && go build . && strip ./cmd && mv ./cmd /build/cadvisor

FROM dadevel/distroless:latest
COPY --from=cadvisor /build/cadvisor ./bin/
RUN ["cadvisor", "-version"]
ENTRYPOINT ["cadvisor", "-logtostderr"]
CMD ["-port", "9338"]

