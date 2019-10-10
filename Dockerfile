FROM python:3.7.4-alpine

RUN apk add git

ENV BASE_DIR=/opt/app
ENV RESULT_DIR=result_dir
ENV RESULT_ROOT_DIR=${BASE_DIR}/${RESULT_DIR}

RUN ln -s /root/.poetry/bin/poetry /usr/bin/poetry && \
    wget https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py && \
    python3 ./get-poetry.py --version 0.12.17 && \
    poetry config settings.virtualenvs.create false && \
    rm ./get-poetry.py

COPY pyproject.toml poetry.lock ${BASE_DIR}/
WORKDIR ${BASE_DIR}/
RUN /bin/sh -c 'poetry install $(test "$CURRENT_ENV" == prod && echo "--no-dev") --no-interaction --no-ansi'

COPY . /opt/app/
