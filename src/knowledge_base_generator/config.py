from pathlib import Path

from pydantic.env_settings import BaseSettings
from pydantic.fields import Field


class Config(BaseSettings):
    app_dir: Path = Path(__file__).absolute().parent

    index_template: str = 'index.html'
    base_page_template: str = 'base_page.html'
    content_dir_name: str = 'content'

    source_ignore: list[str] = Field(default_factory=list)

    # markdown settings
    markdown_extensions = [
        'pymdownx.superfences',
        # It enables code highlight
        'pymdownx.highlight',
        # It enables table support
        'tables',
        # It enables support markdown markup inside html tags
        'md_in_html',
    ]
    markdown_extension_configs = {
        'pymdownx.highlight': {
            'use_pygments': True,
            'noclasses': True,
            'pygments_style': 'friendly',
        },
    }

    class Config:
        project_dir: Path = Path(__file__).absolute().parent.parent.parent
        env_file = project_dir / '.env'


def get_config() -> Config:
    return Config()
