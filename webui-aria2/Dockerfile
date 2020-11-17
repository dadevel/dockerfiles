FROM dadevel/alpine:latest
RUN apk add --no-cache busybox-extras
COPY ./src/docs/ ./static/
COPY ./health.txt ./static/health
USER app
ENTRYPOINT ["httpd", "-f", "-h", "./static"]
CMD ["-p", "8008"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "http://127.0.0.1:8008/health"]
EXPOSE 8008/tcp

