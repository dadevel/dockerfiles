FROM docker.io/library/alpine:latest
RUN apk add --no-cache bash build-base curl git git-lfs neovim python3 shadow && chsh -s /bin/bash root
RUN adduser -h /home/claude -s /bin/bash -D claude && mkdir -p /home/claude/.local/bin
RUN curl -fsSL https://claude.ai/install.sh | bash && cp -H ~/.local/bin/claude /usr/local/bin/ && rm -rf ~/.claude.json ~/.claude ~/.local
USER claude
WORKDIR /workspace
# set storage directory
ENV CLAUDE_CONFIG_DIR=/home/claude/.claude
# disable telemetry and auto-updates
ENV CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=true
ENTRYPOINT ["claude"]
CMD ["--dangerously-skip-permissions"]
VOLUME /home/claude/.claude
