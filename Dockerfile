FROM python:3.13-slim-bookworm

ENV UV_VERSION=0.9.9

WORKDIR /opt/app/

RUN pip install uv==${UV_VERSION}

COPY pyproject.toml uv.lock* ./

RUN uv export -o requirements.txt --no-default-groups --no-hashes --no-annotate --frozen && \
    uv export -o requirements-dev.txt --group dev --no-hashes --no-annotate --frozen

#########################################################################
FROM python:3.13-slim-bookworm

WORKDIR /opt/app/

COPY --from=0 /opt/app/pyproject.toml /opt/app/requirements.txt /opt/app/requirements-dev.txt  ./
RUN pip install -r requirements.txt && rm -rf /root/.cache/pip

COPY src/ /opt/app/src
RUN pip install . && rm -rf /root/.cache/pip

ENTRYPOINT ["markdown-docs-compiler"]
