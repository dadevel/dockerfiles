#!/usr/bin/env bash

INTERVAL="${APT_COLLECTOR_INTERVAL:-3600}"
TEXT_FILE="${APT_COLLECTOR_TEXTFILE_DIR:-/app/cache}/apt.prom"
TEMP_FILE="$TEXT_FILE.$$"
HEALTH_FILE=/dev/shm/healthy

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
    echo '# HELP apt_installed_packages Number of installed apt packages.'
    echo '# TYPE apt_installed_packages gauge'
    echo apt_installed_packages "$(apt list --installed 2> /dev/null | tail -n +2 | wc -l)"

    echo '# HELP apt_upgradeable_packages Number of outdated apt packages.'
    echo '# TYPE apt_upgradeable_packages gauge'
    echo apt_upgradeable_packages "$(apt list --upgradeable 2> /dev/null | tail -n +2 | wc -l)"

    echo '# HELP apt_reboot_required System reboot required to complete software updates.'
    echo '# TYPE apt_reboot_required gauge'
    [[ -f /run/reboot-required ]] && echo apt_reboot_required 1 || echo apt_reboot_required 0
}

apt() {
    command apt -o Debug::NoLocking=1 "$@"
}

main "$@"
