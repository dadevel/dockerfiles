FROM ghcr.io/dadevel/cxx:dev as redis
RUN apt-get update && apt-get install --no-install-recommends -y pkg-config
COPY ./src .
RUN make -j $(nproc)
RUN strip ./src/redis-cli ./src/redis-server

FROM ghcr.io/dadevel/debian:latest
COPY ./redis.conf ./config/
COPY --from=redis /build/src/redis-cli /build/src/redis-server ./bin/
RUN redis-server --version
USER app
ENTRYPOINT ["redis-server", "./config/redis.conf"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["redis-cli", "ping"]
EXPOSE 6379/tcp
VOLUME /app/config /app/data
