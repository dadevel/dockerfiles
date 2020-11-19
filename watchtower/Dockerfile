FROM dadevel/go-builder:latest as watchtower
COPY ./src .
RUN go build .
RUN strip ./watchtower

FROM dadevel/busybox:latest
COPY --from=watchtower /build/watchtower ./bin/
ENTRYPOINT ["watchtower"]

