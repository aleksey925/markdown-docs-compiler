import shutil
from os.path import join, split

from jinja2 import Environment, FileSystemLoader

from config import get_config
from converter import convert_md_files_to_html
from file_utils import clear_dir, CopyTreeRootFilter
from git_utils import pull_repo

conf = get_config()
jinja_env = Environment(loader=FileSystemLoader(conf.JINJA_TEMPLATE_DIR))
jinja_env.globals['STATIC_FILE_PREFIX_PATH'] = conf.STATIC_FILE_PREFIX_PATH
base_knowledge_base_template = jinja_env.get_template(
    conf.BASE_KNOWLEDGE_BASE_TEMPLATE
)


def main():
    if not conf.IS_CI:
        try:
            pull_repo(conf.KNOWLEDGE_BASE_REPO_URL, conf.SOURCE_DIR)
        except Exception:
            print('Возникла ошибка во время извлечения репозитория')
            exit(1)

    clear_dir(conf.RESULT_ROOT_DIR)
    shutil.copytree(
        conf.SOURCE_DIR,
        conf.RESULT_KNOWLEDGE_BASE_DIR,
        ignore=CopyTreeRootFilter(conf.SOURCE_DIR_IGNORE)
    )
    convert_md_files_to_html(
        conf.RESULT_KNOWLEDGE_BASE_DIR, base_knowledge_base_template
    )

    with open(join(conf.RESULT_ROOT_DIR, 'index.html'), 'w') as out:
        out.write(jinja_env.get_template('index.html').render())

    shutil.copytree(
        conf.STATIC_DIR,
        join(conf.RESULT_ROOT_DIR, split(conf.STATIC_DIR)[1])
    )


main()
