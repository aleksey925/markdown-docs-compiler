import shutil
from os.path import join, split

from jinja2 import Environment, FileSystemLoader

from config import (
    BASE_KNOWLEDGE_BASE_TEMPLATE, RESULT_KNOWLEDGE_BASE_DIR,
    KNOWLEDGE_BASE_REPO_URL, SOURCE_DIR, SOURCE_DIR_IGNORE, STATIC_DIR,
    RESULT_ROOT_DIR, STATIC_FILE_PREFIX_PATH, IS_CI, JINJA_TEMPLATE_DIR
)
from converter import convert_md_files_to_html
from file_utils import clear_dir, CopyTreeRootFilter
from git_utils import pull_repo

jinja_env = Environment(loader=FileSystemLoader(JINJA_TEMPLATE_DIR))
jinja_env.globals['STATIC_FILE_PREFIX_PATH'] = STATIC_FILE_PREFIX_PATH
base_knowledge_base_template = jinja_env.get_template(
    BASE_KNOWLEDGE_BASE_TEMPLATE
)


def main():
    if not IS_CI:
        try:
            pull_repo(KNOWLEDGE_BASE_REPO_URL, SOURCE_DIR)
        except Exception:
            print('Возникла ошибка во время извлечения реппозитрия')
            exit(1)

    clear_dir(RESULT_ROOT_DIR)
    shutil.copytree(
        SOURCE_DIR,
        RESULT_KNOWLEDGE_BASE_DIR,
        ignore=CopyTreeRootFilter(SOURCE_DIR_IGNORE)
    )
    convert_md_files_to_html(
        RESULT_KNOWLEDGE_BASE_DIR, base_knowledge_base_template
    )

    with open(join(RESULT_ROOT_DIR, 'index.html'), 'w') as out:
        out.write(jinja_env.get_template('index.html').render())

    shutil.copytree(STATIC_DIR, join(RESULT_ROOT_DIR, split(STATIC_DIR)[1]))


main()
