# Claude

Open current workdir in Claude Code.

~~~ bash
podman run -it --rm -v claude-data:/home/claude/.claude --userns keep-id -v .:/workspace ghcr.io/dadevel/claude
~~~
