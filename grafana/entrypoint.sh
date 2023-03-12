#!/bin/sh
for plugin in $GRAFANA_PLUGINS; do
    if [ ! -d "/app/data/plugins/${plugin}/" ]; then
        echo "installing plugin ${plugin}" && \
            wget -q -O "/app/data/plugins/${plugin}.zip" "https://grafana.com/api/plugins/${plugin}/versions/latest/download" && \
            unzip -q -d /app/data/plugins/ "/app/data/plugins/${plugin}.zip" && \
            rm "/app/data/plugins/${plugin}.zip" || \
            echo "failed to install plugin ${plugin}" >&2
    fi
done
exec grafana server "$@"
