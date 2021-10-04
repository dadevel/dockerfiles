FROM ghcr.io/dadevel/python:latest
COPY ./src/main.py ./bin/aria2-blackhole
COPY ./src/requirements.txt ./static/
RUN pip install -r ./static/requirements.txt && rm ./static/requirements.txt
USER app
ENTRYPOINT ["aria2-blackhole"]
