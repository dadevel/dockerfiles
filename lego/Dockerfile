FROM dadevel/go-builder:latest as lego
ENV GO111MODULE on
COPY ./src .
RUN make build && strip ./dist/lego

FROM dadevel/alpine:latest
COPY --from=lego /build/dist/lego /app/bin/
COPY ./entrypoint.sh /app/bin/
ENTRYPOINT ["entrypoint.sh", "--path", "/app/data"]
USER app

