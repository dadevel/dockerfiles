# Tailscale

Configuration variables:

Name | Default | Description
-----|---------|------------
`TS_AUTHKEY` | none | when persistent storage is availabe
`TS_API_CLIENT_ID` + `TS_API_CLIENT_SECRET` + `TS_TAGS` | none | ephemeral auth key via OAuth when no persistent storage availabe, example tags: `tag:dev,tag:db`
`TS_TUN` | `userspace-networking` |
`TS_SOCKS5_SERVER` | `127.0.0.1:1080` |
`TS_HOSTNAME` | auto |
`TS_EXIT_NODE` | `true` |
`TS_SSH` | `true` |
`TS_SHIELDS_UP` | `false` |
`TS_FWD_LPORT` | `8080` | listen on this TCP port
`TS_FWD_RHOST` + `TS_FWD_RPORT` | none | and forward traffic to this destination, host should be specified by IP
