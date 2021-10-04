FROM mcr.microsoft.com/dotnet/sdk:5.0 as jackett
WORKDIR /build
COPY ./src .
RUN cd ./src/ && dotnet publish Jackett.Server -f net5.0 -r linux-x64 -c Release --self-contained
# -c Debug

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libicu67
COPY --from=jackett /build/src/Jackett.Server/bin/Release/net5.0/linux-x64 ./bin
RUN jackett --version || [ $? -eq 1 ]
USER app
ENV XDG_CONFIG_HOME=/app/data
ENTRYPOINT ["jackett", "--NoRestart", "--NoUpdates"]
CMD ["--ListenPublic"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9117"]
EXPOSE 9117/tcp
