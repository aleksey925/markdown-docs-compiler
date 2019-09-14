import os
from os.path import abspath, dirname, join, exists


def create_dir(base_dir: str, target: str) -> str:
    path = join(base_dir, target)
    if not exists(path):
        os.makedirs(path, exist_ok=True)
    return path


BASE_DIR = abspath(dirname(__file__))

BASE_TEMPLATE = 'base.html'

SOURCE_DIR = create_dir(BASE_DIR, 'source')
SOURCE_DIR_IGNORE = ('.git',)
RESULT_DIR = create_dir(BASE_DIR, 'result_dir')

KNOWLEDGE_BASE_REPO_URL = 'git@gitlab.com:alex925/knowledge-base.git'
