FROM ghcr.io/dadevel/python3:latest as requirements
WORKDIR /build
RUN pip --no-cache-dir install pipenv
COPY ./src/Pipfile ./src/Pipfile.lock .
RUN pipenv lock --keep-outdated --requirements > ./requirements.txt

FROM ghcr.io/dadevel/python3:latest
COPY --from=requirements /build/requirements.txt .
RUN pip --no-cache-dir install -r ./requirements.txt && rm ./requirements.txt
COPY ./src/fritzexporter/ ./fritzexporter/
USER app
ENTRYPOINT ["python", "-m", "fritzexporter", "--config", "./config/fritz-exporter.yaml"]
HEALTHCHECK --interval=60s --timeout=3s CMD ["nc", "-z", "127.0.0.1", "9787"]
EXPOSE 9787/tcp
