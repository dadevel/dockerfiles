FROM dadevel/debian:latest
COPY ./apt.sh ./bin/
COPY ./entrypoint.sh ./lib/
USER app
ENTRYPOINT ["./lib/entrypoint.sh"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["ls", "-d", "/dev/shm/healthy"]

