import pytest

from markdown_docs_compiler.config import Config
from markdown_docs_compiler.converter import convert_md_to_html


def test_convert_md_to_html__send_valid_markdown__return_valid_html(shared_datadir):
    # arrange
    config = Config()
    markdown_text = (shared_datadir / 'markdown_doc.md').read_text()
    expected_html = (shared_datadir / 'html_doc.html').read_text()

    # act
    html = convert_md_to_html(
        markdown_text=markdown_text,
        extensions=config.markdown_extensions,
        extension_configs=config.markdown_extension_configs,
    )

    # assert
    assert html == expected_html


@pytest.mark.parametrize(
    ('markdown', 'expected_id'),
    [
        ('## Реализация dict в CPython', 'реализация-dict-в-cpython'),
        ('## Еще один заголовок', 'еще-один-заголовок'),
        ('## Hello World', 'hello-world'),
        ('## Test_Case', 'test_case'),
        ('## Multiple   Spaces', 'multiple-spaces'),
        ('## Пример! Текст? Пунктуацией.', 'пример-текст-пунктуацией'),
        ('## 123 Numbers', '123-numbers'),
        ('## Кириллица and Latin', 'кириллица-and-latin'),
    ],
)
def test_convert_md_to_html__heading_with_various_text__generate_correct_anchor_id(
    markdown, expected_id
):
    # arrange
    config = Config()

    # act
    html = convert_md_to_html(
        markdown_text=markdown,
        extensions=config.markdown_extensions,
        extension_configs=config.markdown_extension_configs,
    )

    # assert
    assert f'id="{expected_id}"' in html


def test_convert_md_to_html__duplicate_headings__generate_unique_anchor_ids():
    # arrange
    config = Config()
    markdown_text = """## Дубликат

Some text

## Дубликат

More text

## Дубликат
"""

    # act
    html = convert_md_to_html(
        markdown_text=markdown_text,
        extensions=config.markdown_extensions,
        extension_configs=config.markdown_extension_configs,
    )

    # assert
    assert html.count('id="дубликат"') == 1
    assert 'id="дубликат_1"' in html
    assert 'id="дубликат_2"' in html


def test_convert_md_to_html__cyrillic_heading__preserve_cyrillic_in_lowercase():
    # arrange
    config = Config()
    markdown_text = '## БОЛЬШИЕ БУКВЫ ИЗ КИРИЛЛИЦЫ'

    # act
    html = convert_md_to_html(
        markdown_text=markdown_text,
        extensions=config.markdown_extensions,
        extension_configs=config.markdown_extension_configs,
    )

    # assert
    assert 'id="большие-буквы-из-кириллицы"' in html
