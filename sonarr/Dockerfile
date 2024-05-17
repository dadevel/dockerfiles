FROM --platform=$BUILDPLATFORM ghcr.io/dadevel/node:dev as sonarr-web
COPY ./src .
RUN ./build.sh --frontend

FROM mcr.microsoft.com/dotnet/sdk:6.0 as sonarr
WORKDIR /build
COPY ./src .
RUN ./build.sh --backend --runtime linux-x64 --framework net6.0
COPY --from=sonarr-web /build/_output/UI ./_output/UI
RUN ./build.sh --packages --runtime linux-x64 --framework net6.0

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libcurl4 libicu72 libsqlite3-0 mediainfo
COPY --from=sonarr /build/_artifacts/linux-x64/net6.0/Sonarr ./bin
USER app
ENTRYPOINT ["Sonarr", "/nobrowser", "/data=/app/config"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:8989"]
EXPOSE 8989/tcp
VOLUME /app/config
# /app/downloads /app/shows
