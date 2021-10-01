FROM ghcr.io/dadevel/python:latest
RUN apt-get update && apt-get install --no-install-recommends -y smartmontools libcap2-bin && \
setcap -q cap_sys_rawio+ep /usr/sbin/smartctl && \
apt-get purge --auto-remove -y libcap2-bin && \
rm -rf /etc/smartd* && \
addgroup app disk
COPY ./src/smartmon.py ./bin/
COPY ./entrypoint.sh ./lib/
USER app
ENTRYPOINT ["./lib/entrypoint.sh"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["ls", "-d", "/dev/shm/healthy"]