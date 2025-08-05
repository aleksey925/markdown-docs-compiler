FROM python:3.13-slim-bookworm

ENV POETRY_VERSION=2.1.4

WORKDIR /opt/app/

RUN pip install poetry==$POETRY_VERSION \
    && poetry self add poetry-plugin-export \
    && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /opt/app/

RUN poetry export --only=main --without-hashes -o requirements.txt \
    && poetry export --only=dev --without-hashes -o requirements-dev.txt

#########################################################################
FROM python:3.13-slim-bookworm

WORKDIR /opt/app/

COPY --from=0 /opt/app/pyproject.toml /opt/app/requirements.txt /opt/app/requirements-dev.txt  ./
RUN pip install -r requirements.txt && rm -rf /root/.cache/pip

COPY src/ /opt/app/src
RUN pip install . && rm -rf /root/.cache/pip

ENTRYPOINT ["markdown-docs-compiler"]
