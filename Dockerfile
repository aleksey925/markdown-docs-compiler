FROM python:3.10-slim-buster

ENV POETRY_VERSION=1.2.2

WORKDIR /opt/app/

RUN apt update && apt install -y curl
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 - \
    && ln -s /root/.local/bin/poetry /usr/bin/poetry \
    && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /opt/app/

RUN poetry export --only=main --without-hashes -o requirements.txt \
    && poetry export --only=dev --without-hashes -o requirements-dev.txt

##############################################################################################
FROM python:3.10-slim-buster

WORKDIR /opt/app/

COPY --from=0 /opt/app/pyproject.toml /opt/app/requirements.txt /opt/app/requirements-dev.txt  ./
RUN pip install -r requirements.txt && rm -rf /root/.cache/pip

COPY src/ /opt/app/src
RUN pip install . && rm -rf /root/.cache/pip

ENTRYPOINT ["markdown-docs-compiler"]
