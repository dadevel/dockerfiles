FROM docker.io/library/alpine:latest
RUN apk add --no-cache bash build-base curl git git-lfs neovim shadow && chsh -s /bin/bash root
RUN adduser -h /home/claude -s /bin/bash -D claude
RUN curl -fsSL https://claude.ai/install.sh | bash && cp -H ~/.local/bin/claude /usr/local/bin/ && rm -rf ~/.claude.json ~/.claude ~/.local
USER claude
WORKDIR /workspace
ENV CLAUDE_CONFIG_DIR=/home/claude/.claude
ENTRYPOINT ["claude"]
CMD ["--dangerously-skip-permissions"]
VOLUME /home/claude/.claude
