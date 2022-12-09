import typing as t


class CopyTreeRootFilter:
    def __init__(self, ignore_files: t.Iterable[str]) -> None:
        self.is_root_dir = True
        self.ignore_files = ignore_files

    def __call__(self, src: str, files: t.Iterable[str]) -> t.Iterable[str]:
        if self.is_root_dir:
            self.is_root_dir = False
            return self.ignore_files
        return []


def add_closing_slash(path: str) -> str:
    return f'{path}/' if not path.endswith('/') else path
