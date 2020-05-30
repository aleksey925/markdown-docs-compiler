import os
import shutil
from os.path import join, isdir


class CopyTreeRootFilter:
    def __init__(self, list_ignore_files):
        self.is_root = True
        self.list_ignore_files = list_ignore_files

    def __call__(self, src, files):
        if self.is_root:
            self.is_root = False
            return self.list_ignore_files
        return []


def clear_dir(path: str):
    """
    Выполняет рекурсивное удаление всего содержимого дирректории
    :param path: путь к папке
    """
    for i in os.listdir(path):
        cur = join(path, i)
        if isdir(cur):
            shutil.rmtree(cur, ignore_errors=True)
        else:
            os.remove(cur)
