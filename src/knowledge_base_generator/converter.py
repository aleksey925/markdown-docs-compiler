import os
import re
import shutil
import typing as t
from os.path import join
from pathlib import Path

import markdown
from jinja2 import Template


def convert_md_to_html(
    markdown_text: str, extensions: t.Sequence[str], extension_configs: dict[str, t.Any]
) -> str:
    """
    It converts markdown to html.
    """
    html = markdown.markdown(
        markdown_text,
        extensions=extensions,
        extension_configs=extension_configs,
    )
    return re.sub(
        '(<a href=\".*\.)(md)((#.*)?\">)',  # noqa: W605
        r'\g<1>html\g<3>',
        html,
        flags=re.UNICODE | re.MULTILINE,
    )


def convert_md_files_to_html(
    target_path: Path,
    template: Template,
    extensions: t.Sequence[str],
    extension_configs: dict[str, t.Any],
) -> None:
    """
    It converts all markdown files in the target_path to html.
    """
    for root, dirs, files in os.walk(target_path):
        for source_file in filter(lambda i: i.endswith('.md'), files):
            source_file_path = join(root, source_file)
            result_file_path = source_file_path[:-2] + 'html'
            shutil.move(source_file_path, result_file_path)

            with open(result_file_path) as inp:
                markdown_text = inp.read()

            with open(result_file_path, 'w') as out:
                html = convert_md_to_html(
                    markdown_text=markdown_text,
                    extensions=extensions,
                    extension_configs=extension_configs,
                )
                out.write(template.render(data=html))
