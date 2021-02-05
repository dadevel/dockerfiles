FROM dadevel/go-builder:latest as syncthing
COPY ./src .
RUN go run ./build.go -no-upgrade build syncthing
RUN strip ./syncthing
RUN ./syncthing -version

FROM dadevel/busybox:latest
COPY --from=syncthing /build/syncthing ./bin/
ENV HOME /app/data
ENV STGUIADDRESS 0.0.0.0:8384
ENV STNODEFAULTFOLDER true
USER 1000:1000
ENTRYPOINT ["syncthing", "-logfile=-", "-logflags=0", "-home", "./data", "-no-browser", "-no-restart"]
CMD ["-gui-address=:8384"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:8384/"]
EXPOSE 8384/tcp 22000/tcp 21027/udp

