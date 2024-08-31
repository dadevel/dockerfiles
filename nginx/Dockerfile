# documentation: https://nginx.org/en/docs/configure.html

FROM ghcr.io/dadevel/cxx:dev AS nginx
RUN apt-get update && apt-get install --no-install-recommends -y linux-headers-generic libssl-dev libpcre3-dev zlib1g-dev
COPY ./src .
ENV CFLAGS="$CFLAGS -fPIC"
RUN ./auto/configure \
--prefix=/app \
--sbin-path=/app/bin \
--modules-path=/app/lib/nginx/modules \
--conf-path=/app/config/nginx.conf \
--error-log-path=/proc/self/fd/2 \
--http-log-path=/proc/self/fd/1 \
--pid-path=/dev/shm/nginx.pid \
--lock-path=/dev/shm/nginx.lock \
--http-client-body-temp-path=/dev/shm/body \
--http-proxy-temp-path=/dev/shm/proxy \
--http-fastcgi-temp-path=/dev/shm/fastcgi \
--http-uwsgi-temp-path=/dev/shm/uwsgi \
--http-scgi-temp-path=/dev/shm/scgi \
--with-perl_modules_path=/app/lib/perl/vendor_perl \
--user=app \
--group=app \
--without-poll_module \
--without-select_module \
--with-threads \
--with-file-aio \
--with-http_addition_module \
--with-http_auth_request_module \
--with-http_degradation_module \
--with-http_random_index_module \
--with-http_realip_module \
--with-http_secure_link_module \
--with-http_slice_module \
--with-http_ssl_module \
--with-http_stub_status_module \
--with-http_sub_module \
--with-http_v2_module \
--with-mail \
--with-mail_ssl_module \
--with-stream \
--with-stream_realip_module \
--with-stream_ssl_module \
--with-stream_ssl_preread_module
RUN make -j $(nproc)
RUN mv ./objs/nginx .
RUN strip ./nginx
RUN setcap -q cap_net_bind_service+ep ./nginx

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y libssl3 libpcre3 perl zlib1g
COPY ./nginx.conf ./config/
COPY --from=nginx /build/nginx ./bin/
COPY --from=nginx /build/conf/mime.types ./static/
RUN nginx -v
USER app
ENTRYPOINT ["nginx", "-g", "daemon off;", "-c", "./config/nginx.conf"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://127.0.0.1/healthz"]
EXPOSE 80/tcp 443/tcp
VOLUME /app/config
