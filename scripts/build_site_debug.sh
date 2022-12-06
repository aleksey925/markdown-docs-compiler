#!/bin/bash
SOURCE_GIT_REPO=https://gitlab.com/alex925/knowledge-base.git
SOURCE_DIR=$(pwd)/source/
OUTPUT_DIR=$(pwd)/output/

rm -rf "${SOURCE_DIR}"
git clone "${SOURCE_GIT_REPO}" "${SOURCE_DIR}"
knowledge-base-generator build --source-dir "${SOURCE_DIR}" --output-dir "${OUTPUT_DIR}"
