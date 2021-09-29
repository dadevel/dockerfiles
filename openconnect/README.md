# openconnect

[OpenConnect](https://www.infradead.org/openconnect/) docker image with fixes for Pulse Connect Secure from [gitlab.com/webini/openconnect/-/tree/fix/timeout-b](https://gitlab.com/webini/openconnect/-/tree/fix/timeout-b).

## Usage

Start openconnect, ask configuration options interactively.

~~~ bash
docker run -it --rm --network host --device /dev/net/tun --cap-add net_admin ghcr.io/dadevel/openconnect:latest
~~~

To avoid interactive questions fill out the configuration file `./openconnect.env` and append `--env-file ./openconnect.env` to dockers arguments.

If you're running systemd-resolved on your host and want to profit from it's DNS routing feature pass `-v /run/dbus/system_bus_socket:/run/dbus/system_bus_socket` to docker.
