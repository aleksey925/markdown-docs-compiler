from pathlib import Path

import click

from knowledge_base_generator.config import get_config
from knowledge_base_generator.generator import build_site
from knowledge_base_generator.click_preprocessors import (
    path_exists,
    is_dir,
    make_option_preprocessor,
    not_empty_dir,
    empty_dir,
    mkdir,
)


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option(
    '--source-dir',
    required=True,
    type=Path,
    callback=make_option_preprocessor(path_exists, is_dir, not_empty_dir),
    help='Directory with raw markdown files',
)
@click.option(
    '--output-dir',
    required=True,
    type=Path,
    callback=make_option_preprocessor(mkdir, empty_dir),
    help='Directory where the converted files will be placed',
)
@click.option('--site-root-prefix', type=str, default=None)
def build(source_dir: Path, output_dir: Path, site_root_prefix: str | None) -> None:
    build_site(
        config=get_config(),
        source_dir=source_dir,
        output_dir=output_dir,
        site_root_prefix=site_root_prefix
    )


if __name__ == '__main__':
    cli()
