#!/bin/sh

LEGO_SERVER="${LEGO_SERVER:-https://acme-v02.api.letsencrypt.org/directory}"
LEGO_DOMAINS="${LEGO_DOMAINS:?no domains specified}"
LEGO_EMAIL="${LEGO_EMAIL:?no email specified}"
LEGO_KEY_TYPE="${LEGO_KEY_TYPE:-ec384}"
LEGO_MUST_STAPLE="${LEGO_MUST_STAPLE:-false}"
LEGO_GENERATE_DHPARAM="${LEGO_GENERATE_DHPARAM:-false}"

LEGO_CHALLENGE="${LEGO_CHALLENGE:?no challenge specified}"
case "$LEGO_CHALLENGE" in
    http)
        LEGO_HTTP_PORT="${LEGO_HTTP_PORT:-:80}"
        LEGO_HTTP_WEBROOT="${LEGO_HTTP_WEBROOT:-/app/www}"
        ;;
    tls)
        LEGO_TLS_PORT="${LEGO_HTTP_PORT:-:443}"
        ;;
    dns)
        LEGO_DNS_PROVIDER="${LEGO_DNS_PROVIDER:?no dns provider specified}"
        LEGO_DNS_RESOLVERS="${LEGO_DNS_RESOLVERS:-}"
        ;;
esac

LEGO_STORAGE_DIR="${LEGO_STORAGE_DIR:-/app/certs}"
LEGO_REFRESH_INTERVAL="${LEGO_REFRESH_INTERVAL:-7d}"
LEGO_RETRY_INTERVAL="${LEGO_RETRY_INTERVAL:-15m}"
LEGO_RENEW_DAYS="${LEGO_RENEW_DAYS:-30}"

main() {
    update_dhparam
    while :; do
        if update_certificates && update_staples; then
            touch /dev/shm/healthy
            sh -c "$LEGO_RELOAD_COMMAND"
            sleep "$LEGO_REFRESH_INTERVAL"
        else
            rm -f /dev/shm/healthy
            sleep "$LEGO_RETRY_INTERVAL"
        fi
    done
}

update_dhparam() {
    case "$LEGO_GENERATE_DHPARAM" in
        y|yes|true|1)
            [ -f "$LEGO_STORAGE_DIR/certificates/dhparam.pem" ] || openssl dhparam -out "$LEGO_STORAGE_DIR/certificates/dhparam.pem" 2048
            ;;
    esac
}

update_certificates() {
    set -- --path "$LEGO_STORAGE_DIR" --server "$LEGO_SERVER" --accept-tos --email "$LEGO_EMAIL" --key-type "$LEGO_KEY_TYPE"

    for domain in $LEGO_DOMAINS; do
        set -- "$@" --domains "${domain}"
    done

    case "$LEGO_CHALLENGE" in
        http)
            set -- "$@" --http --http.port "$LEGO_HTTP_PORT" --http.webroot "$LEGO_HTTP_WEBROOT"
            ;;
        tls)
            set -- "$@" --tls --tls.port "$LEGO_TLS_PORT"
            ;;
        dns)
            set -- "$@" --dns "$LEGO_DNS_PROVIDER"
            if [ -n "$LEGO_DNS_RESOLVERS" ]; then
                for resolver in $LEGO_DNS_RESOLVERS; do
                    set -- "$@" --dns.resolvers "${resolver}"
                done
            fi
            ;;
    esac

    if [ "$(lego "$@" list)" = "No certificates found." ]; then
        set -- "$@" run
    else
        set -- "$@" renew --reuse-key --days "$LEGO_RENEW_DAYS"
    fi

    case "$LEGO_MUST_STAPLE" in
        y|yes|true|1)
            set -- "$@" --must-staple
            ;;
        *)
            ;;
    esac

    lego "$@"
}

update_staples() {
    case "$LEGO_MUST_STAPLE" in
        y|yes|true|1)
            for path in "$LEGO_STORAGE_DIR"/certificates/*.json; do
                [ -f "${path}" ] || continue
                path="${path%.json}"
                openssl ocsp \
                    -no_nonce \
                    -issuer "${path}.issuer.crt" \
                    -cert "${path}.crt" \
                    -url "$(openssl x509 -noout -ocsp_uri -in "${path}.crt")" \
                    -respout "${path}.staple.der"
            done
            ;;
    esac
}

main "$@"
