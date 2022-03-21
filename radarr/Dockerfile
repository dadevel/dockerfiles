FROM --platform=$BUILDPLATFORM ghcr.io/dadevel/node:dev as radarr-web
COPY ./src .
RUN ./build.sh --frontend

FROM mcr.microsoft.com/dotnet/sdk:6.0 as radarr
WORKDIR /build
COPY ./src .
RUN ./build.sh --backend
COPY --from=radarr-web /build/_output/UI ./_output/UI
RUN ./build.sh --packages --framework net6.0 --runtime linux-x64

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libcurl4 libicu67 libsqlite3-0 mediainfo
COPY --from=radarr /build/_artifacts/linux-x64/net6.0/Radarr ./bin
USER app
ENTRYPOINT ["Radarr", "-nobrowser", "-data=/app/config"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:7878"]
EXPOSE 7878/tcp
VOLUME /app/config
# /app/torrents /app/downloads /app/movies
