FROM ghcr.io/dadevel/go:dev as httpd
COPY ./httpd.go .
RUN go build ./httpd.go
RUN strip ./httpd

FROM ghcr.io/dadevel/debian:latest
COPY ./src/docs ./static/www
COPY ./src/favicon.ico ./static/www/
COPY ./health.txt ./static/www/health
COPY --from=httpd /build/httpd ./bin/
USER app
ENTRYPOINT ["httpd", "-r", "./static/www"]
CMD ["-p", "6801"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:6801/health"]
EXPOSE 6801/tcp
