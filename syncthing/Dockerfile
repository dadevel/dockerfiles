FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache syncthing
ENV HOME=/app/home
ENV STGUIADDRESS=0.0.0.0:8384
ENV STNODEFAULTFOLDER=true
USER app
ENTRYPOINT ["syncthing", "serve", "--logfile=-", "--logflags=0", "--home=/app/config", "--no-browser", "--no-restart"]
CMD ["--gui-address=:8384"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nc", "-z", "localhost", "8384"]
EXPOSE 8384/tcp 22000/tcp 21027/udp
VOLUME /app/config /app/home

