FROM dadevel/python:latest
COPY ./main.py ./bin/nftables-exporter
COPY ./requirements.txt .
RUN apk add --no-cache nftables
RUN pip install -r ./requirements.txt && rm ./requirements.txt
ENTRYPOINT ["nftables-exporter"]
EXPOSE 9630/tcp

