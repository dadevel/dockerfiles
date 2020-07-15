FROM dadevel/python:latest
RUN apk add --no-cache smartmontools && rm -rf /etc/smartd*
COPY ./src/smartmon.py ./entrypoint.sh ./bin/
ENTRYPOINT ["/app/bin/entrypoint.sh"]

