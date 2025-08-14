FROM ghcr.io/dadevel/go:dev AS syncthing
COPY ./src .
RUN go run ./build.go -no-upgrade build syncthing
RUN strip ./syncthing

FROM ghcr.io/dadevel/debian:latest
COPY --from=syncthing /build/syncthing ./bin/
ENV HOME=/app/home
ENV STGUIADDRESS=0.0.0.0:8384
ENV STNODEFAULTFOLDER=true
RUN syncthing version
USER app
ENTRYPOINT ["syncthing", "serve", "--logfile=-", "--logflags=0", "--home=./config", "--no-browser", "--no-restart"]
CMD ["--gui-address=:8384"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nc", "-z", "localhost", "8384"]
EXPOSE 8384/tcp 22000/tcp 21027/udp
VOLUME /app/config /app/home
