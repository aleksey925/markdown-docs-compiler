import os
import shutil
from os.path import join, exists, split, isdir

import git
import markdown
from jinja2 import Environment, FileSystemLoader

from config import (
    BASE_DIR, BASE_TEMPLATE, RESULT_DIR, KNOWLEDGE_BASE_REPO_URL,
    SOURCE_DIR, SOURCE_DIR_IGNORE
)


def pull_repo(repo_url, source_dir: str, pull_error: bool = False):
    if pull_error:
        shutil.rmtree(source_dir, ignore_errors=True)

    if exists(source_dir) and len(os.listdir(source_dir)) == 0:
        git.Repo.clone_from(repo_url, source_dir)
    else:
        try:
            git_repo = git.Repo(source_dir)
            git_repo.remotes.origin.pull()
        except Exception:
            pull_repo(repo_url, source_dir, True)


def clear_dir(path: str):
    for i in os.listdir(path):
        cur = join(path, i)
        if isdir(cur):
            shutil.rmtree(cur, ignore_errors=True)
        else:
            os.remove(cur)


def convert_md_files(source_dir, result_dir, source_dir_ignore, template, css,
                     extension_configs):
    clear_dir(result_dir)

    for root, dirs, files in os.walk(source_dir):
        if any([ignore in root for ignore in source_dir_ignore]):
            continue

        for source_file in filter(lambda i: i.endswith('.md'), files):
            source_file_path = join(root, source_file)
            result_file_path = source_file_path.replace(
                source_dir, result_dir
            )[:-2] + 'html'
            # Если папка не существует, то создаем его
            os.makedirs(split(result_file_path)[0], exist_ok=True)

            with open(source_file_path) as inp, open(result_file_path, 'w') as out:
                html = markdown.markdown(
                    inp.read(),
                    extensions=['pymdownx.superfences', 'pymdownx.highlight'],
                    extension_configs=extension_configs
                )
                out.write(template.render(data=html, css=css))


def rename_filename_in_link():
    pass


jinja_environment = Environment(
    loader=FileSystemLoader('templates'),
)
base_template = jinja_environment.get_template(BASE_TEMPLATE)
css = open(join(BASE_DIR, 'static', 'css', 'base.css')).read()

md_extension_configs = {
    'pymdownx.highlight': {
        'use_pygments': True,
        'noclasses': True,
        'pygments_style': 'friendly',
    },
}

try:
    pull_repo(KNOWLEDGE_BASE_REPO_URL, SOURCE_DIR)
except Exception:
    print('Возникла ошибка во время извлечения реппозитрия')
    exit(1)

convert_md_files(
    SOURCE_DIR, RESULT_DIR, SOURCE_DIR_IGNORE, base_template, css,
    md_extension_configs
)
rename_filename_in_link()
