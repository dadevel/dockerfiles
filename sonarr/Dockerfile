FROM --platform=$BUILDPLATFORM ghcr.io/dadevel/node:dev as sonarr-web
COPY ./src .
COPY ./build.patch .
RUN git apply ./build.patch
RUN bash -c 'source ./build.sh && RunWebpack'

FROM ghcr.io/dadevel/mono:dev as sonarr
COPY ./src .
COPY ./build.patch .
RUN git apply ./build.patch
RUN bash -c 'source ./build.sh && Build'
COPY --from=sonarr-web /build/_output/UI ./_output/UI
RUN bash -c 'source ./build.sh && PackageMono'

FROM ghcr.io/dadevel/mono:latest
RUN apt-get update && apt-get install --no-install-recommends -y libcurl4 libicu63 libsqlite3-0 mediainfo
COPY --from=sonarr /build/_output_linux ./bin
USER app
ENTRYPOINT ["mono", "./bin/Sonarr.exe", "/nobrowser", "/data=/app/config"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:8989"]
EXPOSE 8989/tcp
VOLUME /app/config
# /app/torrents /app/downloads /app/shows
