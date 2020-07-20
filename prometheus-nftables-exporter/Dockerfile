FROM dadevel/python:latest
COPY ./src/main.py ./bin/nftables-exporter
COPY ./src/requirements.txt .
RUN apk add --no-cache nftables
RUN pip install -r ./requirements.txt && rm ./requirements.txt
ENTRYPOINT ["nftables-exporter"]
EXPOSE 9630/tcp

