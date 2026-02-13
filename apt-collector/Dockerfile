FROM ghcr.io/dadevel/debian:latest
COPY ./entrypoint.sh /app/lib/
USER app
ENTRYPOINT ["/app/lib/entrypoint.sh"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["ls", "-d", "/dev/shm/healthy"]
VOLUME /app/textfiles

