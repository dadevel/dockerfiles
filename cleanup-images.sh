#!/usr/bin/env bash
set -euo pipefail

github() {
  echo "$@" >&2
  curl -sSf -H 'Accept: application/vnd.github.v3+json' -u "$GITHUB_USER:$GITHUB_TOKEN" "$@"
}

github_paged() {
    for (( i=1; 1; i++ )); do
        response="$(github "$1&page=${i}&per_page=10")"
        "$(jq -r 'length > 0' <<< "${response}")" || break
        jq -r "$2" <<< "${response}"
    done
}

github_paged 'https://api.github.com/user/packages?package_type=container' '.[].url' | while read -r package_url; do
    if [[ "${package_url}" == */deleted_* ]]; then
        continue
    fi
    github_paged "${package_url}/versions?package_type=container" '.[]|select(.metadata.container.tags | length == 0)|.url' | while read -r version_url; do
        github "${version_url}" -X DELETE 
    done
done
