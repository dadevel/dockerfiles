#!/usr/bin/env bash

main() {
    echo '# HELP apt_installed_packages Number of installed apt packages.'
    echo '# TYPE apt_installed_packages gauge'
    echo apt_installed_packages "$(apt list --installed 2> /dev/null | tail -n +2 | wc -l)"

    echo '# HELP apt_upgradeable_packages Number of outdated apt packages.'
    echo '# TYPE apt_upgradeable_packages gauge'
    echo apt_upgradeable_packages "$(apt list --upgradeable 2> /dev/null | tail -n +2 | wc -l)"

    echo '# HELP apt_reboot_required System reboot required to complete software updates.'
    echo '# TYPE apt_reboot_required gauge'
    [[ -f "$ROOTFS/run/reboot-required" ]] && echo apt_reboot_required 1 || echo apt_reboot_required 0
}

apt() {
    command apt -o Debug::NoLocking=1 "$@"
}

main "$@"

