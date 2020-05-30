import os
from os.path import exists

import git

from file_utils import clear_dir


class GitProgress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        made = round(cur_count / max_count * 100)
        print('\r[{:<25}] {}%'.format('#' * round(made / 4), made), end='')


def pull_repo(repo_url, source_dir: str, pull_error: bool = False):
    if exists(source_dir) and len(os.listdir(source_dir)) == 0:
        print('Клонирование реппозитория:')
        git.Repo.clone_from(repo_url, source_dir, progress=GitProgress())
        print()
    elif pull_error is True:
        exit(1)
    else:
        try:
            print('Извлекаем изменения из реппозитория:')
            git_repo = git.Repo(source_dir)
            git_repo.remotes.origin.pull(progress=GitProgress())
            print()
        except Exception:
            print('\n', 'Возникла ошибка при попытке выполнить git pull')
            clear_dir(source_dir)
            pull_repo(repo_url, source_dir, True)
            return

    print('Извлечение изменений завершено')
