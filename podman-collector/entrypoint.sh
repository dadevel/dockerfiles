#!/bin/sh

INTERVAL="${PODMAN_COLLECTOR_INTERVAL:-60}"
TEXT_FILE="${PODMAN_COLLECTOR_TEXTFILE_DIR:-/app/textfiles}/podman.prom"
TEMP_FILE="$TEXT_FILE.$$"
HEALTH_FILE=/dev/shm/healthy
TEMPLATE='podman_container_state{{`{`}}name="{{.Name}}",state="{{.State.Status}}",health="{{.State.Healthcheck.Status}}"{{`}`}} 1'

main() {
    while :; do
        if collect > "$TEMP_FILE"; then
            mv "$TEMP_FILE" "$TEXT_FILE"
            touch "$HEALTH_FILE"
        else
            echo "error: metric collection failed with exit code $?" >&2
            rm -f "$TEXT_FILE" "$HEALTH_FILE"
        fi
        sleep "$INTERVAL"
    done
}

collect() {
    echo '# HELP podman_container_state Status and health of podman containers.'
    echo '# TYPE podman_container_state gauge'
    podman --remote container ls --all --quiet | xargs -r -- podman --remote container inspect --format "$TEMPLATE"
}

main "$@"
