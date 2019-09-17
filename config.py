import os
from os.path import abspath, dirname, join, exists, split, relpath


def create_dir(base_dir: str, target: str) -> str:
    path = join(base_dir, target)
    if not exists(path):
        os.makedirs(path, exist_ok=True)
    return path


def get_static_file_prefix_path(result_dir, base_dir):
    if os.environ.get('MODE') == 'prod':
        return 'https://aleksey925.github.io/knowledge-base/'
    else:
        # В случае запуска в режиме разработки предпологаем, что web сервер
        # будет считать папку с проектом корнем (Примерно такой url будет
        # получен: /blog-generator/result_dir/ - blog-generator это папка
        # содержащая проект)
        return '/' + relpath(result_dir, split(base_dir)[0]) + '/'


BASE_DIR = abspath(dirname(__file__))

BASE_KNOWLEDGE_BASE_TEMPLATE = 'knowledge-base.html'
STATIC_DIR = join(BASE_DIR, 'static')

SOURCE_DIR = create_dir(BASE_DIR, 'source')
SOURCE_DIR_IGNORE = ('.git', '.gitignore')
RESULT_ROOT_DIR = create_dir(BASE_DIR, 'result_dir')

STATIC_FILE_PREFIX_PATH = get_static_file_prefix_path(
    RESULT_ROOT_DIR, BASE_DIR
)

KNOWLEDGE_BASE_REPO_URL = 'git@gitlab.com:alex925/knowledge-base.git'
RESULT_KNOWLEDGE_BASE_DIR = create_dir(RESULT_ROOT_DIR, 'knowledge_base')
