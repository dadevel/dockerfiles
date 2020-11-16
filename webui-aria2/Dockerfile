FROM dadevel/alpine:latest
RUN apk add --no-cache busybox-extras
COPY ./src/docs/ /app/srv/
USER app
ENTRYPOINT ["httpd", "-f", "-h", "/app/srv"]
CMD ["-p", "8080"]
EXPOSE 8080/tcp

