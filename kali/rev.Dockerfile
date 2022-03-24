FROM ghcr.io/dadevel/kali:std
COPY ./rev.txt ./pkgs.txt
RUN grep -v -e '^#' -e '^$' ./pkgs.txt | xargs -r -- apt-get install --no-install-recommends -y --
