#!/usr/bin/env bash
set -eu

DIR="${BLACKHOLE_WATCH_DIR:-./cache}"
ENDPOINT="${ARIA2_ENDPOINT:-http://localhost:6800/jsonrpc}"
TOKEN="${ARIA2_API_TOKEN?-api token missing}"
BODY='{
  jsonrpc: "2.0",
  id: $id,
  method: "aria2.addTorrent",
  "params": [$token, $content, [], {}]
}'

inotifywait --quiet --monitor --recursive --event modify --format '%f/%w%n' "${DIR:-1}" | while read -r file; do
    if [[ "${file}" == *.torrent ]]; then
        echo "pushing ${file}" >&2
        jq \
            --arg id "$(date +torrentwatcher-%s | base64 -w 0)" \
            --arg token "token:$TOKEN" \
            --arg content "$(< "${file}")" \
            "$BODY" <<< '{}' | \
            curl -sSf "$ENDPOINT" -H 'Content-Type: application/json;charset=UTF-8' -H 'Accept: application/json' --data-binary @- && \
            rm -f "${file}"
    fi
done
