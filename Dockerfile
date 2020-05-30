FROM python:3.7.4-alpine

ARG MODE=${MODE}
ENV BASE_DIR=/opt/app \
    RESULT_DIR=result_dir \
    POETRY_VERSION=1.0.5
ENV RESULT_ROOT_DIR=${BASE_DIR}/${RESULT_DIR}

RUN apk add git

RUN ln -s /root/.poetry/bin/poetry /usr/bin/poetry && \
    wget https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py && \
    python3 ./get-poetry.py --version $POETRY_VERSION && \
    poetry config virtualenvs.create false && \
    rm ./get-poetry.py

COPY pyproject.toml poetry.lock ${BASE_DIR}/
WORKDIR ${BASE_DIR}/
RUN /bin/sh -c 'poetry install $(test "$MODE" == prod && echo "--no-dev") --no-interaction --no-ansi'

COPY . /opt/app/
