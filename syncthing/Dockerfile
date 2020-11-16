FROM dadevel/go-builder:latest as syncthing
COPY ./src/ .
RUN go run ./build.go -no-upgrade build syncthing && strip ./syncthing

FROM dadevel/distroless:latest
COPY --from=syncthing /build/syncthing ./bin/
ENV STGUIADDRESS 0.0.0.0:8384
ENV STNODEFAULTFOLDER true
USER 1000:1000
RUN ["syncthing", "-version"]
ENTRYPOINT ["syncthing", "-logfile=-", "-logflags=0", "-home", "./data", "-no-browser", "-no-restart"]
CMD ["-gui-address=:8384"]
EXPOSE 8384/tcp 22000/tcp 21027/udp

