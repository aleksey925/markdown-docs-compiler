import typing as t
from pathlib import Path

import click
from click.core import Context, Option

T = t.TypeVar('T')


def make_option_preprocessor(
    *preprocessors: t.Callable[[T], T],
) -> t.Callable[[t.Any, t.Any, T], T]:
    def inner(ctx: Context, param: Option, value: T) -> T:
        for func in preprocessors:
            try:
                value = func(value)
            except Exception as exc:
                raise click.BadParameter(str(exc))

        return value

    return inner


def path_exists(value: Path) -> Path:
    if not value.exists():
        raise ValueError('Path not exits')

    return value


def mkdir(value: Path) -> Path:
    value.mkdir(parents=True, exist_ok=True)
    return value


def is_dir(value: Path) -> Path:
    if not value.is_dir():
        raise ValueError('Directory required')

    return value


def empty_dir(value: Path) -> Path:
    if len(list(value.iterdir())) > 0:
        raise ValueError('Directory must be empty')

    return value


def not_empty_dir(value: Path) -> Path:
    if len(list(value.iterdir())) == 0:
        raise ValueError('Directory must not be empty')

    return value
