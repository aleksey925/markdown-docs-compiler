from pathlib import Path
from typing import Any, ClassVar

from pydantic.env_settings import BaseSettings
from pydantic.fields import Field
from pymdownx import slugs


def linkify_callback(
    attrs: dict[tuple[str | None, str], str], new: bool
) -> dict[tuple[str | None, str], str] | None:
    href = attrs.get((None, 'href'), '')
    if href.startswith('mailto:'):
        return None

    if (
        href.startswith(('http://', 'https://'))
        or href.startswith('www.')
        or href.startswith('ftp://')
    ):
        attrs[(None, 'target')] = '_blank'
        attrs[(None, 'rel')] = 'noopener noreferrer'

    return attrs


class Config(BaseSettings):
    app_dir: Path = Path(__file__).absolute().parent

    index_template: str = 'index.html'
    base_page_template: str = 'base_page.html'
    content_dir_name: str = 'content'

    source_ignore: list[str] = Field(default_factory=list)

    # markdown settings
    markdown_extensions: ClassVar[list[str]] = [
        'pymdownx.superfences',
        # It enables code highlight
        'pymdownx.highlight',
        # It enables table support
        'tables',
        # It enables support markdown markup inside html tags
        'md_in_html',
        # It enables lists without preceding blank line (GitHub-style)
        'markdown_docs_compiler.extensions.breakless_lists',
        # It enables automatic anchor generation for headings (GitHub-compatible)
        'toc',
        # It enables automatic URL detection and linkification
        'mdx_linkify',
    ]
    markdown_extension_configs: ClassVar[dict[str, Any]] = {
        'pymdownx.highlight': {
            'use_pygments': True,
            'noclasses': True,
            'pygments_style': 'friendly',
        },
        'toc': {
            'slugify': slugs.slugify(case='lower'),
            'separator': '-',
        },
        'mdx_linkify': {
            'linker_options': {
                'callbacks': [linkify_callback],
            },
        },
    }

    class Config:
        project_dir: Path = Path(__file__).absolute().parent.parent.parent
        env_file = project_dir / '.env'


def get_config() -> Config:
    return Config()
