FROM debian:13-slim AS exporter

RUN apt-get update  \
    && apt-get -y --no-install-recommends install \
       sudo curl git ca-certificates build-essential \
    && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV MISE_DATA_DIR="/mise"
ENV MISE_CONFIG_DIR="/mise"
ENV MISE_CACHE_DIR="/mise/cache"
ENV MISE_INSTALL_PATH="/usr/local/bin/mise"
ENV PATH="/mise/shims:$PATH"

COPY mise.toml ./

RUN curl https://mise.run | sh && \
    mise trust && \
    mise i

WORKDIR /opt/app/

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
