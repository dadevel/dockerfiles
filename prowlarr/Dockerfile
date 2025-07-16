FROM --platform=$BUILDPLATFORM ghcr.io/dadevel/node:dev AS prowlarr-web
COPY ./src .
RUN ./build.sh --frontend

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS prowlarr
WORKDIR /build
COPY ./src .
RUN ./build.sh --backend
COPY --from=prowlarr-web /build/_output/UI ./_output/UI
RUN ./build.sh --packages --framework net8.0 --runtime linux-x64

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libcurl4 libicu72 libsqlite3-0 mediainfo
COPY --from=prowlarr /build/_artifacts/linux-x64/net8.0/Prowlarr ./bin
USER app
ENTRYPOINT ["Prowlarr", "-nobrowser", "-data=/app/config"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9696"]
EXPOSE 9696/tcp
VOLUME /app/config
# /app/downloads /app/movies
