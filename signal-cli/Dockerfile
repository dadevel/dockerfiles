FROM docker.io/library/gradle:jre14 as signal-cli
WORKDIR /build
COPY ./src .
RUN ./gradlew build
RUN ./gradlew installDist

FROM docker.io/library/openjdk:14-slim
ARG PREFIX=/app
ARG PUID=1000
ARG PGID=1000
ARG TIMEZONE=UTC
ARG LANGUAGE=en_US
ARG CHARSET=UTF-8
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
apt-get install --no-install-recommends -y ca-certificates locales tzdata wget && \
ln -sf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && \
localedef -i $LANGUAGE -c -f $CHARSET -A /usr/share/locale/locale.alias $LANGUAGE.$CHARSET && \
groupadd --gid $PGID app && \
useradd --uid $PUID --gid $PGID --comment '' --home-dir /dev/shm --no-create-home --shell /bin/bash --no-log-init app && \
mkdir -p $PREFIX/bin $PREFIX/lib $PREFIX/static $PREFIX/config $PREFIX/data $PREFIX/cache $PREFIX/storage && \
chown -R $PUID:$PGID $PREFIX/data $PREFIX/cache $PREFIX/storage
ENV PATH=$PREFIX/bin:$PATH \
LD_LIBRARY_PATH=$PREFIX/lib \
HOME=/dev/shm \
XDG_RUNTIME_DIR=/dev/shm \
TMPDIR=/dev/shm \
LANG=$LANGUAGE.$CHARSET \
LANGUAGE=$LANGUAGE \
CHARSET=$CHARSET \
TZ=$TIMEZONE
WORKDIR $PREFIX
COPY --from=signal-cli /build/build/install/signal-cli/bin/ ./bin/
COPY --from=signal-cli /build/build/install/signal-cli/lib/ ./lib/
RUN signal-cli --version
ENTRYPOINT ["signal-cli"]
CMD ["--help"]
