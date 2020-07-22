FROM debian:stable-slim
WORKDIR /app
COPY ./apt.sh ./entrypoint.sh ./bin/
RUN useradd --uid 1000 --user-group --home-dir /app/data --no-create-home --no-log-init app && \
mkdir ./data && chown -R app:app ./data
ENV PATH $PATH:/app/bin
# apt requires a writeable temp directory
ENV TMPDIR /dev/shm
ENTRYPOINT ["entrypoint.sh"]
USER app
VOLUME /app/data /rootfs

