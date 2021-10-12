FROM --platform=$BUILDPLATFORM ghcr.io/dadevel/node:dev as bazarr-web
COPY ./src/frontend .
RUN npm install
RUN npm run build

# bazarr supports only python 3.8, 3.9 works anyway, 3.10 throws exceptions
FROM ghcr.io/dadevel/cxx:dev as bazarr
RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-dev python3-pip python3-venv libffi-dev
RUN python3 -m venv ./venv
COPY ./src/requirements.txt .
RUN ./venv/bin/pip3 install -r ./requirements.txt

FROM ghcr.io/dadevel/debian:latest
RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-distutils libffi7 unrar-free ffmpeg
COPY ./src/libs/ ./lib/libs/
COPY ./src/bazarr/ ./lib/bazarr/
COPY ./src/bazarr.py ./lib/
COPY --from=bazarr-web /build/build/ ./lib/frontend/build/
COPY --from=bazarr /build/venv/ ./venv/
USER app
ENTRYPOINT ["./venv/bin/python3", "./lib/bazarr.py", "--no-update", "--config", "./data"]
CMD ["--port", "6767"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["wget", "-q", "-O", "-", "http://localhost:6767"]
EXPOSE 6767/tcp
VOLUME /app/data
