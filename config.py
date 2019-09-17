import os
from os.path import abspath, dirname, join, exists


def create_dir(base_dir: str, target: str) -> str:
    path = join(base_dir, target)
    if not exists(path):
        os.makedirs(path, exist_ok=True)
    return path


BASE_DIR = abspath(dirname(__file__))

BASE_KNOWLEDGE_BASE_TEMPLATE = 'knowledge-base.html'
STATIC_DIR = join(BASE_DIR, 'static')

SOURCE_DIR = create_dir(BASE_DIR, 'source')
SOURCE_DIR_IGNORE = ('.git', '.gitignore')
RESULT_ROOT_DIR = create_dir(BASE_DIR, 'result_dir')

STATIC_FILE_PREFIX_PATH = 'https://aleksey925.github.io/knowledge-base/'

KNOWLEDGE_BASE_REPO_URL = 'git@gitlab.com:alex925/knowledge-base.git'
RESULT_KNOWLEDGE_BASE_DIR = create_dir(RESULT_ROOT_DIR, 'knowledge_base')
