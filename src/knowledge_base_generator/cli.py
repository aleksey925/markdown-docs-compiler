from pathlib import Path

import click

from knowledge_base_generator.click_preprocessors import (
    empty_dir,
    is_dir,
    make_option_preprocessor,
    mkdir,
    not_empty_dir,
    path_exists,
)
from knowledge_base_generator.config import get_config
from knowledge_base_generator.main import compile_site


@click.group()
def cli() -> None:
    pass


@cli.command(name='compile')
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
@click.option(
    '--template-dir',
    required=True,
    type=Path,
    callback=make_option_preprocessor(path_exists, is_dir),
    help='Directory jinja templates',
)
@click.option(
    '--static-dir',
    required=True,
    type=Path,
    callback=make_option_preprocessor(path_exists, is_dir),
    help='Directory with static files',
)
@click.option('--site-root-prefix', type=str, default=None)
def compile_(
    source_dir: Path,
    output_dir: Path,
    template_dir: Path,
    static_dir: Path,
    site_root_prefix: str | None,
) -> None:
    compile_site(
        config=get_config(),
        source_dir=source_dir,
        output_dir=output_dir,
        template_dir=template_dir,
        static_dir=static_dir,
        site_root_prefix=site_root_prefix,
    )


if __name__ == '__main__':
    cli()
