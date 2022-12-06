from knowledge_base_generator.config import Config
from knowledge_base_generator.converter import convert_md_to_html


def test_convert_md_to_html__send_valid_markdown__return_valid_html(
        shared_datadir
):
    # arrange
    config = Config()
    markdown_text = (shared_datadir / 'markdown_doc.md').read_text()
    expected_html = (shared_datadir / 'html_doc.html').read_text()

    # act
    html = convert_md_to_html(
        markdown_text=markdown_text,
        extensions=config.markdown_extensions,
        extension_configs=config.markdown_extension_configs
    )

    # assert
    assert html == expected_html
