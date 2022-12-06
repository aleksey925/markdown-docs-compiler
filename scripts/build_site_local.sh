#!/bin/bash
SOURCE_GIT_REPO=https://gitlab.com/alex925/knowledge-base.git
SOURCE_DIR=$(pwd)/source/

OUTPUT_GET_REPO=https://github.com/aleksey925/knowledge-base.git
OUTPUT_DIR=$(pwd)/output/
SITE_ROOT_PREFIX=https://aleksey925.github.io/knowledge-base/

rm -rf "${SOURCE_DIR}"
git clone "${SOURCE_GIT_REPO}" "${SOURCE_DIR}"
knowledge-base-generator build \
                         --source-dir "${SOURCE_DIR}"\
                         --output-dir "${OUTPUT_DIR}"\
                         --site-root-prefix="${SITE_ROOT_PREFIX}"

cd "${OUTPUT_DIR}" && \
   git init && \
   git add . && \
   git commit -m 'init' && \
   git remote add origin "${OUTPUT_GET_REPO}" && \
   git push -u origin master -f
