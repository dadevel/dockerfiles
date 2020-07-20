FROM dadevel/python:latest
COPY ./src/smartmon.py ./entrypoint.sh ./bin/
RUN apk add --no-cache libcap smartmontools && \
setcap -q cap_sys_rawio+ep /usr/sbin/smartctl && \
apk del --purge --rdepends libcap && \
rm -rf /etc/smartd* && \
addgroup app disk
ENTRYPOINT ["entrypoint.sh"]
USER app:app

