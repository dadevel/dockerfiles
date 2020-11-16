FROM dadevel/debian:latest
COPY ./apt.sh ./bin/
COPY ./entrypoint.sh ./lib/
USER app
ENTRYPOINT ["./lib/entrypoint.sh"]

