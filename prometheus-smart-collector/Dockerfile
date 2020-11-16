FROM dadevel/python:latest
RUN apk add --no-cache libcap smartmontools && \
setcap -q cap_sys_rawio+ep /usr/sbin/smartctl && \
apk del --purge --rdepends libcap && \
rm -rf /etc/smartd* && \
addgroup app disk
COPY ./src/smartmon.py ./bin/
COPY ./entrypoint.sh ./lib/
USER app
ENTRYPOINT ["./lib/entrypoint.sh"]

