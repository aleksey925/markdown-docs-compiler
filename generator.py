import os
import re
import shutil
from os.path import join, exists, isdir, split

import git
import markdown
from jinja2 import Environment, FileSystemLoader

from config import (
    BASE_KNOWLEDGE_BASE_TEMPLATE, RESULT_KNOWLEDGE_BASE_DIR,
    KNOWLEDGE_BASE_REPO_URL, SOURCE_DIR, SOURCE_DIR_IGNORE, STATIC_DIR,
    RESULT_ROOT_DIR, STATIC_FILE_PREFIX_PATH, IS_CI, JINJA_TEMPLATE_DIR
)


class GitProgress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        made = round(cur_count / max_count * 100)
        print('\r[{:<25}] {}%'.format('#' * round(made / 4), made), end='')


def pull_repo(repo_url, source_dir: str, pull_error: bool = False):
    if exists(source_dir) and len(os.listdir(source_dir)) == 0:
        print('Клонирование реппозитория:')
        git.Repo.clone_from(repo_url, source_dir, progress=GitProgress())
        print()
    elif pull_error is True:
        exit(1)
    else:
        try:
            print('Извлекаем изменения из реппозитория:')
            git_repo = git.Repo(source_dir)
            git_repo.remotes.origin.pull(progress=GitProgress())
            print()
        except Exception:
            print('\n', 'Возникла ошибка при попытке выполнить git pull')
            clear_dir(source_dir)
            pull_repo(repo_url, source_dir, True)
            return

    print('Извлечение изменений завершено')


class CopyTreeRootFilter:
    def __init__(self, list_ignore_files):
        self.is_root = True
        self.list_ignore_files = list_ignore_files

    def __call__(self, src, files):
        if self.is_root:
            self.is_root = False
            return self.list_ignore_files
        return []


def clear_dir(path: str):
    for i in os.listdir(path):
        cur = join(path, i)
        if isdir(cur):
            shutil.rmtree(cur, ignore_errors=True)
        else:
            os.remove(cur)


def convert_md_files(result_dir, template, extensions, extension_configs):
    for root, dirs, files in os.walk(result_dir):
        for source_file in filter(lambda i: i.endswith('.md'), files):
            source_file_path = join(root, source_file)
            result_file_path = source_file_path[:-2] + 'html'
            shutil.move(source_file_path, result_file_path)

            with open(result_file_path) as inp:
                markdown_str = inp.read()

            with open(result_file_path, 'w') as out:
                html = markdown.markdown(
                    markdown_str,
                    extensions=extensions,
                    extension_configs=extension_configs
                )
                out.write(template.render(data=html))


def rename_filename_in_links(result_dir):
    for root, dirs, files in os.walk(result_dir):
        for file_name in filter(lambda i: i.endswith('.html'), files):
            file_path = join(root, file_name)

            with open(file_path) as f:
                file_data = f.read()

            with open(file_path, 'w') as f:
                f.write(re.sub(
                    '(<a href=\".*\.)(md)((#.*)?\">)',
                    r'\g<1>html\g<3>',
                    file_data,
                    flags=re.UNICODE | re.MULTILINE
                ))


jinja_environment = Environment(
    loader=FileSystemLoader(JINJA_TEMPLATE_DIR),
)
jinja_environment.globals['STATIC_FILE_PREFIX_PATH'] = STATIC_FILE_PREFIX_PATH
base_knowledge_base_template = jinja_environment.get_template(
    BASE_KNOWLEDGE_BASE_TEMPLATE
)

md_extensions = [
    'pymdownx.superfences',
    'pymdownx.highlight',
    'tables',
]
md_extension_configs = {
    'pymdownx.highlight': {
        'use_pygments': True,
        'noclasses': True,
        'pygments_style': 'friendly',
    },
}

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
convert_md_files(
    RESULT_KNOWLEDGE_BASE_DIR, base_knowledge_base_template,
    md_extensions, md_extension_configs
)
rename_filename_in_links(RESULT_KNOWLEDGE_BASE_DIR)

with open(join(RESULT_ROOT_DIR, 'index.html'), 'w') as out:
    out.write(
        jinja_environment.get_template('index.html').render()
    )

shutil.copytree(STATIC_DIR, join(RESULT_ROOT_DIR, split(STATIC_DIR)[1]))
