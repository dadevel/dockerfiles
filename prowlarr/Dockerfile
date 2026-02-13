FROM docker.io/library/alpine:latest AS src
WORKDIR /build
RUN apk add --no-cache git
RUN git clone https://github.com/prowlarr/prowlarr.git . && \
git checkout "$(git tag | grep '^v' | sort -Vu | tail -n1)"

FROM docker.io/library/node:20-alpine AS web
WORKDIR /build
RUN apk add --no-cache bash
COPY --from=src /build/ .
RUN ./build.sh --frontend

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS prowlarr
WORKDIR /build
COPY --from=src /build/ .
RUN ./build.sh --backend
COPY --from=web /build/_output/UI ./_output/UI
RUN ./build.sh --packages --framework net8.0 --runtime linux-musl-x64

FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache libcurl icu-libs sqlite-libs mediainfo
COPY --from=prowlarr /build/_artifacts/linux-musl-x64/net8.0/Prowlarr /app/bin
USER app
ENTRYPOINT ["Prowlarr", "-nobrowser", "-data=/app/config"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9696"]
EXPOSE 9696/tcp
VOLUME /app/config
# /app/downloads /app/movies

