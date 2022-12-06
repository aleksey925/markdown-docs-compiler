class CopyTreeRootFilter:
    def __init__(self, list_ignore_files):
        self.is_root = True
        self.list_ignore_files = list_ignore_files

    def __call__(self, src, files):
        if self.is_root:
            self.is_root = False
            return self.list_ignore_files
        return []


def add_closing_slash(path: str) -> str:
    return f'{path}/' if not path.endswith('/') else path
