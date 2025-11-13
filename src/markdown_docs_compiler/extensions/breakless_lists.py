"""
Markdown extension to allow lists without a preceding empty line.

Based on: https://github.com/adamb70/mdx-breakless-lists
"""

import re
from typing import Any

from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class BreaklessLists(Extension):
    def extendMarkdown(self, md: Markdown) -> None:  # noqa: N802
        md.preprocessors.register(BreaklessListsProcessor(md.parser), 'breakless_lists', 27)
        md.registerExtension(self)


class BreaklessListsProcessor(Preprocessor):
    """
    Simply add an extra line break before the list and let the other
    processors handle list creation.
    """

    def __init__(self, parser: Any) -> None:
        super().__init__(parser)
        self.tab_length = parser.md.tab_length
        self.LI_RE = re.compile(r'^[ \t]*>?[ \t]*((\d+\.)|[*+-])[ \t]+.*$')

    def run(self, lines: list[str]) -> list[str]:
        previous_was_li = False
        in_codefence = False
        new_lines: list[str] = []

        for line in lines:
            if line.startswith('```'):
                in_codefence = not in_codefence

            if self.LI_RE.match(line) and not in_codefence:
                if not previous_was_li:
                    new_lines.append('')
                previous_was_li = True
            elif line == '':
                previous_was_li = False

            new_lines.append(line)

        return new_lines


def makeExtension(**kwargs: Any) -> BreaklessLists:  # noqa: N802
    return BreaklessLists(**kwargs)
