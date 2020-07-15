#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar lastpipe

# configuration options
declare -gr REPO_URL=https://github.com/dadevel/dockerfiles
declare -gr REGISTRY_NAME=docker.io
declare -gr REGISTRY_USER=dadevel
declare -gr PLATFORM="${PLATFORM:-linux/amd64,linux/arm64,linux/arm/v7}"
declare -gr CACHE="$PWD/.cache"

setup() {
    if [[ " $(id --groups --name) " == *\ docker\ * ]]; then
        declare -gri SUDO=0
    else
        declare -gri SUDO=1
    fi
    # setup when running on github actions
    if [[ -v CI ]]; then
        run_silent docker login "$REGISTRY_NAME" --username "$REGISTRY_USER" --password-stdin <<< "${REGISTRY_TOKEN:?authentication token is missing}"
        git config user.name github-actions
        git config user.email github-actions@github.com
    fi
    # setup docker buildx with qemu
    run_silent docker run --rm --privileged multiarch/qemu-user-static:latest --reset --persistent yes
    docker buildx inspect multiarch &> /dev/null || \
        run_silent docker buildx create --name multiarch --use && \
        run_silent docker buildx inspect --bootstrap multiarch
}

teardown() {
    declare -i rc="$?"
    if [[ -v CI ]]; then
        run_silent docker logout "$REGISTRY_NAME"
    fi
    exit "${rc}"
}

main() {
    declare -g IMAGE_NAME=''
    declare -g BUILD_DATE=''
    declare -g SOURCE_URL=''
    declare -g LATEST_REF='' 
    declare -g LATEST_VERSION=''
    declare -g MAJOR_VERSION=''
    declare -g LATEST_COMMIT=''
    declare -g CURRENT_COMMIT=''
    while (( $# )); do
        process "$1"
        IMAGE_NAME=''
        BUILD_DATE=''
        SOURCE_URL=''
        LATEST_REF='' 
        LATEST_VERSION=''
        MAJOR_VERSION=''
        LATEST_COMMIT=''
        CURRENT_COMMIT=''
        shift
    done
}

process() {
    IMAGE_NAME="$(basename "$1")"
    BUILD_DATE="$(date --utc +%Y-%m-%dT%H:%M:%SZ)"
    if [[ -d "$1/src" && -f "$1/Dockerfile" ]]; then
        fetch "$1"
        checkout "$1"
        build "$1"
        bump "$1"
    elif [[ -f "$1/Dockerfile" ]]; then
        build "$1"
    else
        echo 'build target does not exist' >&2
        return 1
    fi
}

fetch() {
    # update source
    run git submodule --quiet update --init --recursive "$1/src"
    SOURCE_URL="$(git config "submodule.$1/src.url")"
    # load version regex
    source "$1/meta.env"
    declare -r ref_matcher="${ref_matcher:?variable not defined in meta.env}"
    declare -r version_adapter="${version_adapter:-}"
    # find newest version
    declare ref latest_ref latest_version major_version
    git -C "$1/src" show-ref | cut -d ' ' -f 2- | sort --version-sort | while read -r ref; do
        if [[ "${ref}" =~ ${ref_matcher} ]]; then
            latest_ref="${ref}"
            latest_version="$(sed "${version_adapter}" <<< "${BASH_REMATCH[1]:-}")"
            major_version="$(sed "${version_adapter}" <<< "${BASH_REMATCH[2]:-}")"
        fi
    done
    # set variables
    LATEST_REF="${latest_ref:?no ref matched}"
    LATEST_VERSION="${latest_version}"
    MAJOR_VERSION="${major_version}"
    LATEST_COMMIT="$(git -C "$1/src" rev-list --max-count=1 "$LATEST_REF")"
    CURRENT_COMMIT="$(git -C "$1/src" rev-parse HEAD)"
    echo "current commit ${CURRENT_COMMIT:0:7}, latest commit ${LATEST_COMMIT:0:7}, latest reference $LATEST_REF, latest version ${LATEST_VERSION:-unknown}, major version ${MAJOR_VERSION:-unknown}"
}

checkout() {
    run git -C "$1/src" fetch --quiet origin "$LATEST_REF"
    run git -C "$1/src" checkout --quiet "$LATEST_REF"
}

build() {
    declare -a args=(
        --tag "$REGISTRY_NAME/$REGISTRY_USER/$IMAGE_NAME:latest"
        --label "org.opencontainers.image.authors=$REGISTRY_USER"
        --label "org.opencontainers.image.url=$REPO_URL"
        --label "org.opencontainers.image.created=$BUILD_DATE"
    )
    if [[ -n "$LATEST_VERSION" ]]; then
        args+=(
            --tag "$REGISTRY_NAME/$REGISTRY_USER/$IMAGE_NAME:$LATEST_VERSION"
            --label "org.opencontainers.image.title=$IMAGE_NAME v$LATEST_VERSION"
            --label "org.opencontainers.image.version=$LATEST_VERSION"
        )
    else
        args+=(--label "org.opencontainers.image.title=$IMAGE_NAME")
    fi
    [[ -z "$MAJOR_VERSION" ]] || args+=(--tag "$REGISTRY_NAME/$REGISTRY_USER/$IMAGE_NAME:$MAJOR_VERSION")
    [[ -z "$SOURCE_URL" ]] || args+=(--label "org.opencontainers.image.source=$SOURCE_URL")
    [[ -z "$LATEST_COMMIT" ]] || args+=(--label "org.opencontainers.image.revision=$LATEST_COMMIT")
    run docker buildx build \
        --cache-from "type=local,src=$CACHE" \
        --cache-to "type=local,dest=$CACHE" \
        --platform "$PLATFORM" \
        --push \
        "${args[@]}" "$1"
}

bump() {
    if [[ "$LATEST_COMMIT" != "$CURRENT_COMMIT" ]]; then
        run git add "$1/src"
        if [[ -n "$LATEST_VERSION" ]]; then
            run git commit --quiet --message "$IMAGE_NAME: bump version to v$LATEST_VERSION"
        else
            run git commit --quiet --message "$IMAGE_NAME: bump version to ${LATEST_COMMIT:0:7}"
        fi
        run git push --quiet
    fi
}

docker() {
    declare -xr DOCKER_BUILDKIT=1
    declare -xr DOCKER_CLI_EXPERIMENTAL=enabled
    (( SUDO )) && sudo --preserve-env=DOCKER_BUILDKIT,DOCKER_CLI_EXPERIMENTAL -- docker "$@" || command docker "$@"
}

run_silent() {
    echo "$@"
    "$@" > /dev/null
}

run() {
    echo "$@"
    "$@"
}

setup
trap teardown EXIT
main "$@"

