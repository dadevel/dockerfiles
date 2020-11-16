FROM dadevel/python:latest
RUN apk add --no-cache libcap nftables && \
setcap -q cap_net_admin+ep /usr/sbin/nft && \
apk del --purge --rdepends libcap && \
rm -rf /etc/nftables*
COPY ./src/main.py ./bin/nftables-exporter
COPY ./src/requirements.txt ./static/
RUN pip install -r ./static/requirements.txt && rm ./static/requirements.txt
USER app
ENTRYPOINT ["nftables-exporter"]
EXPOSE 9630/tcp

