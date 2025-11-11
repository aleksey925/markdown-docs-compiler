from markdown import Markdown


def test_breakless_lists__list_after_text__creates_separate_list():
    # arrange
    md = Markdown(extensions=['markdown_docs_compiler.extensions.breakless_lists'])
    markdown_text = """Text before list:
- Item 1
- Item 2"""

    # act
    html = md.convert(markdown_text)

    # assert
    expected = '<p>Text before list:</p>\n<ul>\n<li>Item 1</li>\n<li>Item 2</li>\n</ul>'
    assert html == expected


def test_breakless_lists__list_after_bold_text__creates_separate_list():
    # arrange
    md = Markdown(extensions=['markdown_docs_compiler.extensions.breakless_lists'])
    markdown_text = """**Result:**
- Item 1
- Item 2"""

    # act
    html = md.convert(markdown_text)

    # assert
    expected = '<p><strong>Result:</strong></p>\n<ul>\n<li>Item 1</li>\n<li>Item 2</li>\n</ul>'
    assert html == expected


def test_breakless_lists__numbered_list_after_text__creates_separate_list():
    # arrange
    md = Markdown(extensions=['markdown_docs_compiler.extensions.breakless_lists'])
    markdown_text = """Steps:
1. First step
2. Second step"""

    # act
    html = md.convert(markdown_text)

    # assert
    expected = '<p>Steps:</p>\n<ol>\n<li>First step</li>\n<li>Second step</li>\n</ol>'
    assert html == expected


def test_breakless_lists__list_inside_code_fence__not_processed():
    # arrange
    md = Markdown(extensions=['markdown_docs_compiler.extensions.breakless_lists'])
    markdown_text = """Config:
```yaml
items:
- item1
- item2
```"""

    # act
    html = md.convert(markdown_text)

    # assert
    # without fenced_code extension, ``` becomes inline code
    expected = '<p>Config:\n<code>yaml\nitems:\n- item1\n- item2</code></p>'
    assert html == expected


def test_breakless_lists__list_inside_blockquote__creates_list():
    # arrange
    md = Markdown(extensions=['markdown_docs_compiler.extensions.breakless_lists'])
    markdown_text = """Quote with list:
> - Item 1
> - Item 2"""

    # act
    html = md.convert(markdown_text)

    # assert
    expected = (
        '<p>Quote with list:</p>\n'
        '<blockquote>\n'
        '<ul>\n'
        '<li>Item 1</li>\n'
        '<li>Item 2</li>\n'
        '</ul>\n'
        '</blockquote>'
    )
    assert html == expected


def test_breakless_lists__list_with_tabs__becomes_code_block():
    # arrange
    md = Markdown(extensions=['markdown_docs_compiler.extensions.breakless_lists'])
    markdown_text = 'Text:\n\t- Item 1\n\t- Item 2'

    # act
    html = md.convert(markdown_text)

    # assert
    # tab at line start creates code block in markdown
    expected = '<p>Text:</p>\n<pre><code>- Item 1\n- Item 2\n</code></pre>'
    assert html == expected


def test_breakless_lists__code_fence_with_backticks__single_line_becomes_inline_code():
    # arrange
    md = Markdown(extensions=['markdown_docs_compiler.extensions.breakless_lists'])
    markdown_text = """First code:
```
- code item
```

Real list:
- Real item

Second code:
```yaml
- another code item
```"""

    # act
    html = md.convert(markdown_text)

    # assert
    # without fenced_code extension, ``` becomes inline code
    expected = (
        '<p>First code:\n'
        '<code>- code item</code></p>\n'
        '<p>Real list:</p>\n'
        '<ul>\n'
        '<li>Real item</li>\n'
        '</ul>\n'
        '<p>Second code:\n'
        '<code>yaml\n'
        '- another code item</code></p>'
    )
    assert html == expected


def test_breakless_lists__empty_lines_reset_state__works_correctly():
    # arrange
    md = Markdown(extensions=['markdown_docs_compiler.extensions.breakless_lists'])
    markdown_text = """First list:
- Item 1

Second list:
- Item 2"""

    # act
    html = md.convert(markdown_text)

    # assert
    expected = (
        '<p>First list:</p>\n'
        '<ul>\n'
        '<li>Item 1</li>\n'
        '</ul>\n'
        '<p>Second list:</p>\n'
        '<ul>\n'
        '<li>Item 2</li>\n'
        '</ul>'
    )
    assert html == expected


def test_breakless_lists__mixed_list_markers__creates_single_list():
    # arrange
    md = Markdown(extensions=['markdown_docs_compiler.extensions.breakless_lists'])
    markdown_text = """Using asterisk:
* Item A

Using plus:
+ Item B

Using minus:
- Item C"""

    # act
    html = md.convert(markdown_text)

    # assert
    expected = (
        '<p>Using asterisk:</p>\n'
        '<ul>\n'
        '<li>Item A</li>\n'
        '</ul>\n'
        '<p>Using plus:</p>\n'
        '<ul>\n'
        '<li>Item B</li>\n'
        '</ul>\n'
        '<p>Using minus:</p>\n'
        '<ul>\n'
        '<li>Item C</li>\n'
        '</ul>'
    )
    assert html == expected


def test_breakless_lists__original_problem__creates_list():
    # arrange
    md = Markdown(extensions=['markdown_docs_compiler.extensions.breakless_lists'])
    markdown_text = """**Результат:**
- `CUSTOM_DATA_PATH = "/path/to/.venv/data"`
- `PYTHONPATH = "/path/to/.venv/src"`"""

    # act
    html = md.convert(markdown_text)

    # assert
    expected = (
        '<p><strong>Результат:</strong></p>\n'
        '<ul>\n'
        '<li><code>CUSTOM_DATA_PATH = "/path/to/.venv/data"</code></li>\n'
        '<li><code>PYTHONPATH = "/path/to/.venv/src"</code></li>\n'
        '</ul>'
    )
    assert html == expected
