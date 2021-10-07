FROM ghcr.io/dadevel/python:latest
COPY ./src/main.py ./bin/aria2-blackhole
COPY ./src/requirements.txt .
RUN pip install -r ./requirements.txt && rm ./requirements.txt
USER app
ENTRYPOINT ["aria2-blackhole"]
VOLUME /app/torrents /app/downloads /app/files
