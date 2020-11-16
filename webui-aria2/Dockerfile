FROM dadevel/alpine:latest
RUN apk add --no-cache busybox-extras
COPY ./src/docs/ ./static/
USER app
ENTRYPOINT ["httpd", "-f", "-h", "./static"]
CMD ["-p", "8080"]
EXPOSE 8080/tcp

