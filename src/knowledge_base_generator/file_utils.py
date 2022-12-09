import typing as t


class CopyTreeRootFilter:
    def __init__(self, list_ignore_files: t.Iterable[str]) -> None:
        self.is_root = True
        self.list_ignore_files = list_ignore_files

    def __call__(self, src: str, files: t.Iterable[str]) -> t.Iterable[str]:
        if self.is_root:
            self.is_root = False
            return self.list_ignore_files
        return []


def add_closing_slash(path: str) -> str:
    return f'{path}/' if not path.endswith('/') else path
