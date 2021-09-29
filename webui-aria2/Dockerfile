FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y busybox
COPY ./src/docs ./static/www
COPY ./health.txt ./static/www/health
USER app
ENTRYPOINT ["busybox", "httpd", "-f", "-h", "./static/www"]
CMD ["-p", "6801"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:6801/health"]
EXPOSE 6801/tcp
