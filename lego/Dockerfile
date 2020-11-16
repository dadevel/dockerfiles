FROM dadevel/go-builder:latest as lego
ENV GO111MODULE on
COPY ./src/ .
RUN make build && strip ./dist/lego

FROM dadevel/alpine:latest
RUN apk add --no-cache openssl
COPY --from=lego /build/dist/lego ./bin/
COPY ./entrypoint.sh ./lib/
USER app
ENTRYPOINT ["./lib/entrypoint.sh", "--path", "./data"]

