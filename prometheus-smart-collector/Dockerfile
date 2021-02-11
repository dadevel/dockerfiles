FROM ghcr.io/dadevel/python3:latest
RUN apk add --no-cache smartmontools libcap && \
setcap -q cap_sys_rawio+ep /usr/sbin/smartctl && \
apk del --purge --rdepends libcap && \
rm -rf /etc/smartd* && \
addgroup app disk
COPY ./src/smartmon.py ./bin/
COPY ./entrypoint.sh ./lib/
USER app
ENTRYPOINT ["./lib/entrypoint.sh"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["ls", "-d", "/dev/shm/healthy"]

