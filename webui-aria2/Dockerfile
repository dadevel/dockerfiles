FROM dadevel/alpine:latest
RUN apk add --no-cache busybox-extras
COPY ./src/docs ./static/www
COPY ./health.txt ./static/www/health
USER app
ENTRYPOINT ["httpd", "-f", "-h", "./static/www"]
CMD ["-p", "6801"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:6801/health"]
EXPOSE 6801/tcp

