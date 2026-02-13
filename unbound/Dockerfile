FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache unbound && setcap -q cap_net_bind_service+ep $(which unbound)
RUN wget -q -O - https://www.internic.net/domain/named.cache | tee /app/cache/root.hints | awk '{ if ($3 == "A" || $3 == "AAAA") { printf("master: %s\n", $NF) } }' > /app/cache/root.conf && { unbound-anchor -a /app/cache/root.key -r /app/cache/root.hints || [ $? -eq 1 ]; } && chown -R app:app /app/cache
COPY ./unbound.conf /app/config/
USER app
ENTRYPOINT ["unbound", "-dd", "-c", "/app/config/unbound.conf"]
CMD ["-p"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nslookup", "health.unbound.test", "127.0.0.1"]
EXPOSE 53/tcp 53/udp 853/tcp
VOLUME /app/config /app/cache

