FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache nginx && setcap -q cap_net_bind_service+ep $(which nginx)
COPY ./nginx.conf /app/config/
USER app
ENTRYPOINT ["nginx", "-g", "daemon off;", "-c", "/app/config/nginx.conf"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1/healthz"]
EXPOSE 80/tcp 443/tcp
VOLUME /app/config

