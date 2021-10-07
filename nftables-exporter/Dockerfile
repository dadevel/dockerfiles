FROM ghcr.io/dadevel/python:latest
RUN apt-get install --no-install-recommends -y nftables libcap2-bin && \
setcap -q cap_net_admin+ep /usr/sbin/nft && \
apt-get purge --auto-remove -y libcap2-bin && \
rm -rf /etc/nftables*
COPY ./src/main.py ./bin/nftables-exporter
COPY ./src/requirements.txt .
RUN pip install -r ./requirements.txt && rm ./requirements.txt
USER app
ENTRYPOINT ["nftables-exporter"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:9630/health"]
EXPOSE 9630/tcp
