FROM ghcr.io/dadevel/python3:latest
RUN apk add --no-cache nftables libcap && \
setcap -q cap_net_admin+ep /usr/sbin/nft && \
apk del --purge --rdepends libcap && \
rm -rf /etc/nftables*
COPY ./src/main.py ./bin/nftables-exporter
COPY ./src/requirements.txt ./static/
RUN pip install -r ./static/requirements.txt && rm ./static/requirements.txt
USER app
ENTRYPOINT ["nftables-exporter"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:9630/health"]
EXPOSE 9630/tcp

