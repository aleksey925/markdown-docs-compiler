import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from knowledge_base_generator.config import Config
from knowledge_base_generator.converter import convert_md_files_to_html
from knowledge_base_generator.file_utils import CopyTreeRootFilter, add_closing_slash


def build_site(*, config: Config, source_dir: Path, output_dir: Path, site_root_prefix: str | None = None):
    source_dir = source_dir.absolute()
    output_dir = output_dir.absolute()
    site_root_prefix = add_closing_slash(site_root_prefix or f'{output_dir}/')

    jinja_env = Environment(loader=FileSystemLoader(config.template_dir))
    jinja_env.globals['SITE_ROOT_PREFIX'] = site_root_prefix
    jinja_env.globals['CONTENT_DIR_NAME'] = config.content_dir_name

    base_template = jinja_env.get_template(config.base_page_template)
    index_template = jinja_env.get_template(config.index_template)

    path_to_target_files = output_dir / config.content_dir_name
    shutil.copytree(
        source_dir,
        path_to_target_files,
        ignore=CopyTreeRootFilter(config.source_dir_ignore)
    )
    convert_md_files_to_html(
        target_path=path_to_target_files,
        template=base_template,
        extensions=config.markdown_extensions,
        extension_configs=config.markdown_extension_configs,
    )

    with open(output_dir / config.index_template, 'w') as out:
        out.write(index_template.render())

    shutil.copytree(
        config.static_dir,
        output_dir / config.static_dir.name
    )
