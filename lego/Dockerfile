FROM dadevel/go-builder:latest as lego
ENV GO111MODULE on
COPY ./src .
RUN make build
RUN strip ./dist/lego

FROM dadevel/alpine:latest
RUN apk add --no-cache libressl
COPY --from=lego /build/dist/lego ./bin/
COPY ./entrypoint.sh ./lib/
USER app
ENTRYPOINT ["./lib/entrypoint.sh", "--path", "./data"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["ls", "-d", "/dev/shm/healthy"]

