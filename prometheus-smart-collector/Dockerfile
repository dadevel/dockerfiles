FROM dadevel/python:latest
COPY ./src/smartmon.py ./entrypoint.sh ./bin/
RUN apk add --no-cache libcap smartmontools && \
setcap -q cap_sys_rawio+ep ./smartmon.py && \
apk del --purge --rdepends libcap && \
rm -rf /etc/smartd*
ENTRYPOINT ["entrypoint.sh"]

