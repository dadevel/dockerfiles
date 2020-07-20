FROM dadevel/python:latest
COPY ./src/main.py ./bin/nftables-exporter
COPY ./src/requirements.txt .
RUN apk add --no-cache libcap nftables && \
setcap -q cap_net_admin+ep ./bin/nftables-exporter && \
apk del --purge --rdepends libcap
RUN pip install -r ./requirements.txt && rm ./requirements.txt
ENTRYPOINT ["nftables-exporter"]
USER app:app
EXPOSE 9630/tcp

