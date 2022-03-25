FROM ghcr.io/dadevel/cxx:dev as massdns
RUN git clone --depth 1 https://github.com/blechschmidt/massdns.git .
RUN make
RUN strip ./bin/massdns

FROM ghcr.io/dadevel/go:dev as puredns
ENV GO111MODULE=on
COPY ./src .
RUN go build -v
RUN strip ./puredns

FROM ghcr.io/dadevel/debian:latest
COPY --from=massdns /build/bin/massdns ./bin/
COPY --from=puredns /build/puredns ./bin/
RUN puredns --version
USER app
ENTRYPOINT ["puredns"]
CMD ["--help"]
