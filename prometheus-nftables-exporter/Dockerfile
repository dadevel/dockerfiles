FROM dadevel/python:latest
COPY ./src/main.py ./bin/nftables-exporter
COPY ./src/requirements.txt .
RUN apk add --no-cache libcap nftables && \
setcap -q cap_net_admin+ep /usr/sbin/nft && \
apk del --purge --rdepends libcap && \
rm -rf /etc/nftables*
RUN pip install -r ./requirements.txt && rm ./requirements.txt
ENTRYPOINT ["nftables-exporter"]
USER app:app
EXPOSE 9630/tcp

