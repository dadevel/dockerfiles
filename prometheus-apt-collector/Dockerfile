FROM debian:stable-slim
WORKDIR /app
RUN useradd --uid 1000 --user-group --home-dir /app/data --no-create-home --no-log-init app && \
mkdir ./data && chown -R app:app ./data
COPY ./apt.sh ./entrypoint.sh ./bin/
ENTRYPOINT ["entrypoint.sh"]
ENV PATH $PATH:/app/bin
# apt requires a writeable temp directory
ENV TMPDIR /dev/shm
USER app
VOLUME /app/data

