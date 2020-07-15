FROM dadevel/go-builder:latest as watchtower
COPY ./src/ .
RUN go build . && strip ./watchtower

FROM dadevel/distroless:latest
COPY --from=watchtower /build/watchtower /app/bin/
ENTRYPOINT ["watchtower"]
VOLUME /var/run/docker.sock

