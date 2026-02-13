FROM ghcr.io/dadevel/alpine:latest AS src
WORKDIR /build
RUN apk add --no-cache git
RUN git clone https://github.com/ziahamza/webui-aria2.git .

FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache busybox-extras
COPY --from=src /build/docs /app/static/www
COPY --from=src /build/favicon.ico /app/static/www/
COPY ./health.txt /app/static/www/health
USER app
ENTRYPOINT ["httpd", "-f", "-h", "/app/static/www"]
CMD ["-p", "6801"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:6801/health"]
EXPOSE 6801/tcp

