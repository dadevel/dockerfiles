FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache chrony && setcap -q cap_net_bind_service,cap_sys_time+ep $(which chronyd)
COPY ./chrony.conf /app/config/
USER app
ENTRYPOINT ["chronyd", "-d", "-U", "-f", "/app/config/chrony.conf"]
CMD ["-L", "1", "-r", "-s"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["chronyc", "sources"]
EXPOSE 123/udp
VOLUME /app/config /app/cache

