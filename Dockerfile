FROM python:3.7.4-alpine

RUN apk add git

RUN ln -s /root/.poetry/bin/poetry /usr/bin/poetry && \
    wget https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py && \
    python3 ./get-poetry.py --version 0.12.17 && \
    poetry config settings.virtualenvs.create false && \
    rm ./get-poetry.py

COPY pyproject.toml poetry.lock /opt/app/
WORKDIR /opt/app/
RUN /bin/sh -c 'poetry install $(test "$CURRENT_ENV" == prod && echo "--no-dev") --no-interaction --no-ansi'

COPY . /opt/app/
