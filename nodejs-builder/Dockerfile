FROM node:12-alpine
RUN apk add --no-cache ca-certificates git make tzdata && \
ln -s /usr/share/zoneinfo/UTC /etc/localtime
ENV CHARSET UTF-8
ENV LANG C.UTF-8
ENV TZ UTC
WORKDIR /build

