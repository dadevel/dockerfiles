FROM ghcr.io/dadevel/alpine:latest
RUN wget -O /app/bin/smartmon.py https://raw.githubusercontent.com/prometheus-community/node-exporter-textfile-collector-scripts/76a66171683889a3cb43f1b8fe6cf5d5067ff927/smartmon.py && chmod +x /app/bin/smartmon.py
RUN apk add --no-cache python3 py3-prometheus-client smartmontools && \
rm -rf /etc/smartd* && \
setcap -q cap_sys_rawio+ep $(which smartctl) && \
addgroup app disk
COPY ./entrypoint.sh /app/lib/
USER app
ENTRYPOINT ["/app/lib/entrypoint.sh"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["ls", "-d", "/dev/shm/healthy"]
VOLUME /app/textfiles

