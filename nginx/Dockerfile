FROM dadevel/c-builder:latest as nginx
RUN apk add --no-cache gd-dev geoip-dev libmaxminddb-dev libxml2-dev libxslt-dev linux-headers openssl-dev pcre-dev perl-dev pkgconf zlib-dev
COPY ./src .
ENV CFLAGS $CFLAGS -fPIC
RUN ./auto/configure \
--prefix=/app \
--sbin-path=/app/bin \
--modules-path=/app/lib/nginx/modules \
--with-perl_modules_path=/app/lib/perl5/vendor_perl \
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
--user=app \
--group=app \
--with-threads \
--with-file-aio \
--with-http_ssl_module \
--with-http_v2_module \
--with-http_realip_module \
--with-http_addition_module \
--with-http_xslt_module=dynamic \
--with-http_image_filter_module=dynamic \
--with-http_geoip_module=dynamic \
--with-http_sub_module \
--with-http_dav_module \
--with-http_flv_module \
--with-http_mp4_module \
--with-http_gunzip_module \
--with-http_gzip_static_module \
--with-http_auth_request_module \
--with-http_random_index_module \
--with-http_secure_link_module \
--with-http_degradation_module \
--with-http_slice_module \
--with-http_stub_status_module \
--with-mail=dynamic \
--with-mail_ssl_module \
--with-stream=dynamic \
--with-stream_ssl_module \
--with-stream_realip_module \
--with-stream_geoip_module=dynamic \
--with-stream_ssl_preread_module
RUN make -j $(nproc) && strip ./objs/nginx

FROM dadevel/alpine:latest
COPY --from=nginx /build/objs/nginx /app/bin/
COPY --from=nginx /build/conf/mime.types /app/static/
RUN apk add --no-cache openssl pcre perl zlib
RUN nginx -v
ENTRYPOINT ["nginx", "-g", "daemon off;"]
EXPOSE 80/tcp 443/tcp
USER app

