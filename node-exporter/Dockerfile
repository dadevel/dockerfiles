FROM ghcr.io/dadevel/alpine:latest
RUN apk add --no-cache prometheus-node-exporter
USER app
ENTRYPOINT ["node_exporter", "--collector.textfile.directory=/app/textfiles", "--path.rootfs=/rootfs", "--path.sysfs=/rootfs/sys", "--path.procfs=/rootfs/proc", "--path.udev.data=/rootfs/run/udev/data"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:9100/"]
EXPOSE 9100/tcp
VOLUME /app/config /app/textfiles

