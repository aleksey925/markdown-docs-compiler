from converter import convert_md_to_html


def test_convert_md_to_html__send_valid_markdown__return_valid_html(
        shared_datadir
):
    markdown_text = (shared_datadir / 'markdown_doc.md').read_text()
    expected_html = (shared_datadir / 'html_doc.html').read_text()
    html = convert_md_to_html(markdown_text)

    assert html == expected_html
