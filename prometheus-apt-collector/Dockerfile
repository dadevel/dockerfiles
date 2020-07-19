FROM debian:stable-slim
WORKDIR /app
COPY ./apt.sh ./entrypoint.sh ./bin/
RUN mkdir ./data
ENV PATH $PATH:/app/bin
ENTRYPOINT ["entrypoint.sh"]
VOLUME /app/data

