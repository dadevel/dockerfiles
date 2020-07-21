FROM debian:stable-slim
WORKDIR /app
COPY ./apt.sh ./entrypoint.sh ./bin/
RUN useradd --uid 1000 --user-group --home-dir /app/data --no-create-home --no-log-init app && \
mkdir ./data && chown -R app:app ./data && \
chmod 0700 ./data
ENV PATH $PATH:/app/bin
ENTRYPOINT ["entrypoint.sh"]
USER app
VOLUME /app/data /rootfs

