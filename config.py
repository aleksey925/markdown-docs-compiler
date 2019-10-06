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


def get_or_create_source_dir(base_dir, is_ci) -> str:
    if is_ci:
        return join('/builds', os.environ.get('CI_PROJECT_PATH'))
    else:
        return create_dir(base_dir, 'source')


BASE_DIR = abspath(dirname(__file__))
IS_CI = True if os.environ.get('CI') == 'true' else False

BASE_KNOWLEDGE_BASE_TEMPLATE = 'knowledge-base.html'
STATIC_DIR = join(BASE_DIR, 'static')

SOURCE_DIR = get_or_create_source_dir(BASE_DIR, IS_CI)
SOURCE_DIR_IGNORE = ('.git', '.gitignore', '.gitlab-ci.yml')
RESULT_ROOT_DIR = create_dir(BASE_DIR, 'result_dir')

STATIC_FILE_PREFIX_PATH = get_static_file_prefix_path(
    RESULT_ROOT_DIR, BASE_DIR
)

KNOWLEDGE_BASE_REPO_URL = 'git@gitlab.com:alex925/knowledge-base.git'
RESULT_KNOWLEDGE_BASE_DIR = create_dir(RESULT_ROOT_DIR, 'knowledge_base')
