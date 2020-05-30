import os
import re
import shutil
from os.path import join

import markdown
from jinja2 import Template

from config import get_config


conf = get_config()


def convert_md_to_html(markdown_text: str) -> str:
    """
    Конвертирует markdown строку в html
    :param markdown_text: строка содержащая markdown разметку
    :return: конвертированная строка
    """
    html = markdown.markdown(
        markdown_text,
        extensions=conf.MARKDOWN_EXTENSIONS,
        extension_configs=conf.MARKDOWN_EXTENSION_CONFIGS
    )
    return re.sub(
        '(<a href=\".*\.)(md)((#.*)?\">)',
        r'\g<1>html\g<3>',
        html,
        flags=re.UNICODE | re.MULTILINE
    )


def convert_md_files_to_html(target_path: str, template: Template):
    """
    Функция выполняющая рекурсивную конвертацию всех markdown файлов
    расположенных в target_path. Кроме конвертации, так выполняется исправление
    ссылок на файлы (меняется расширение у файла с md на html).
    :param target_path: путь к папке в которой расположены markdown файлы,
    которые необходимо конвертировать
    :param template: jinja2 шаблон внутрь которого будут вставлен результат
    конвертации
    """
    for root, dirs, files in os.walk(target_path):
        for source_file in filter(lambda i: i.endswith('.md'), files):
            source_file_path = join(root, source_file)
            result_file_path = source_file_path[:-2] + 'html'
            shutil.move(source_file_path, result_file_path)

            with open(result_file_path) as inp:
                markdown_text = inp.read()

            with open(result_file_path, 'w') as out:
                html = convert_md_to_html(markdown_text)
                out.write(template.render(data=html))
