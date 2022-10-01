FROM docker.io/library/python:2-slim
WORKDIR /app
COPY ./src .
RUN pip install -r ./requirements.txt
ENTRYPOINT ["python2", "-m", "peas"]
CMD ["--help"]
