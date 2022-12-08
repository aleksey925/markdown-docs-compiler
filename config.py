import os
from os.path import abspath, dirname, join, exists, split, relpath


class BaseConfig:
    def __init__(self):
        self.MODE = os.environ.get('MODE')

        self.IS_CI = True if os.environ.get('CI') == 'true' else False
        self.CI_PROJECT_PATH = os.environ.get('CI_PROJECT_PATH')

        self.BASE_DIR = os.environ.get('BASE_DIR', abspath(dirname(__file__)))
        self.RESULT_DIR = os.environ.get('RESULT_DIR', 'result_dir')
        self.RESULT_ROOT_DIR = self.create_dir(
            join(self.BASE_DIR, self.RESULT_DIR)
        )

        self.BASE_KNOWLEDGE_BASE_TEMPLATE = 'knowledge-base.html'
        self.JINJA_TEMPLATE_DIR = join(self.BASE_DIR, 'templates')
        self.STATIC_DIR = join(self.BASE_DIR, 'static')

        self.SOURCE_DIR = self.get_or_create_source_dir(self.BASE_DIR, self.IS_CI)
        self.SOURCE_DIR_IGNORE = (
            '.git', '.gitignore', '.gitlab-ci.yml', '.dockerignore', '.build-deps'
        )

        self.KNOWLEDGE_BASE_REPO_URL = (
            'git@gitlab.com:alex925/knowledge-base.git'
        )
        self.RESULT_KNOWLEDGE_BASE_DIR = self.create_dir(
            join(self.RESULT_ROOT_DIR, 'knowledge_base')
        )

        # MARKDOWN
        self.MARKDOWN_EXTENSIONS = [
            'pymdownx.superfences',
            # Включает подстветку кода
            'pymdownx.highlight',
            # Включает поддержку таблиц
            'tables',
            # Позволяет размещать markdown разметку внутри html тегов
            'md_in_html',
        ]
        self.MARKDOWN_EXTENSION_CONFIGS = {
            'pymdownx.highlight': {
                'use_pygments': True,
                'noclasses': True,
                'pygments_style': 'friendly',
            },
        }

    def create_dir(self, path) -> str:
        if not exists(path):
            os.makedirs(path, exist_ok=True)
        return path

    def get_or_create_source_dir(self, base_dir: str, is_ci: bool) -> str:
        source_dir = join(base_dir, 'source')
        if is_ci:
            root_clone_knowledge_base = join('/builds', self.CI_PROJECT_PATH)
            os.symlink(root_clone_knowledge_base, source_dir)
        else:
            self.create_dir(source_dir)

        return source_dir


class DevConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        # В случае запуска в режиме разработки предполагаем, что web сервер
        # будет считать папку с проектом корнем (Примерно такой url будет
        # получен: /blog-generator/result_dir/ - blog-generator это папка
        # содержащая проект)
        self.STATIC_FILE_PREFIX_PATH = (
            f'/{relpath(self.RESULT_ROOT_DIR, split(self.BASE_DIR)[0])}/'
        )


class ProdConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.STATIC_FILE_PREFIX_PATH = (
            'https://aleksey925.github.io/knowledge-base/'
        )


config = {
    'dev': DevConfig,
    'prod': ProdConfig
}


def _get_config_gen():
    conf = config[os.environ.get('MODE', 'dev')]()
    while True:
        yield conf


_config_gen = _get_config_gen()
next(_config_gen)


def get_config():
    return next(_config_gen)
