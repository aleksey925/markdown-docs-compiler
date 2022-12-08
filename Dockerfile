FROM python:3.10-slim-buster

ENV POETRY_VERSION=1.2.2

WORKDIR /opt/app/

RUN apt update \
    && apt upgrade -y \
    && apt install -y curl \
    && ln -s /root/.local/bin/poetry /usr/bin/poetry \
    && curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 - \
    && poetry config virtualenvs.create false \
    && apt purge -y curl \
    && apt autoremove -y \
    && apt autoclean -y \
    && rm -fr /var/lib/apt/lists /var/lib/cache/* /var/log/*

COPY pyproject.toml poetry.lock /opt/app/
COPY src/ /opt/app/src

RUN poetry install --only main --no-interaction --no-ansi

ENTRYPOINT ["knowledge-base-generator"]
