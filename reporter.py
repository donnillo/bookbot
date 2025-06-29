import enum
import pathlib
from collections.abc import Callable
from dataclasses import dataclass
from contextlib import redirect_stdout
from io import StringIO
from textwrap import wrap
from typing import Literal

from paths import APP_NAME
from paths import Path


def get_book_text(path: Path) -> str:
    return pathlib.Path(path).read_text()


@dataclass(slots=True)
class TitleFormatProps:
    fill: str
    align: Literal["<", "^", ">"]
    transform: Callable[[str], str] | None = None

    def __post_init__(self):
        if len(self.fill) != 1:
            raise ValueError("Fill character can only be a of length 1.")


class TitleFormat(TitleFormatProps, enum.Enum):
    TOP = "=", "^", str.upper
    SUB = "-", "^", str.title


class Width:
    def __init__(self, *, min: int):
        self.minimum = min

    def __set_name__(self, owner, name):
        self.name = owner.__name__

    def __get__(self, instance, owner=None):
        if owner is not None:
            return getattr(self, owner.__name__, self.minimum)
        return getattr(self, instance.__class__.__name__, self.minimum)

    def __set__(self, instance, value: int):
        if value < self.minimum:
            raise ValueError(
                f"{self.name} width cannot be less than {self.minimum}.")
        setattr(self, instance.__class__.__name__, value)


class Block:
    tf: TitleFormatProps
    width: Width = Width(min=20)
    content: StringIO
    title: str = ""
    footer: str | None = None

    def _render_title(self, msg: str = ""):
        if msg:
            msg = f" {msg} "
        if self.tf.transform:
            msg = self.tf.transform(msg)
        return f"{msg:{self.tf.fill}{self.tf.align}{self.width}}"

    def __enter__(self):
        self.stdout = redirect_stdout(StringIO())
        self.content = self.stdout.__enter__()
        print(self._render_title(self.title))
        return self

    def __exit__(self, *exc):
        if self.footer is not None:
            print(self._render_title(self.footer))
        self.stdout.__exit__(*exc)
        self._flush_content()

    def _flush_content(self):
        for line in self.content.getvalue().splitlines():
            if len(line) > self.width:
                for line in wrap(line, width=self.width):
                    print(line)
            else:
                print(line)

    def set_width(self, width: int):
        self.width = width
        return self


class MainBlock(Block):
    tf = TitleFormat.TOP
    title = APP_NAME
    footer = "end"


class StatBlock(Block):
    tf = TitleFormat.SUB

    def __get__(self, instance, _):
        self.book = instance.book
        self.width = instance.width
        return self

    def __call__(self, stat_func: Callable, **stat_func_kwargs):
        self.title = stat_func.__name__.replace("_", " ")
        self.output = stat_func(self.book, **stat_func_kwargs)
        return self

    def __enter__(self):
        self = super().__enter__()
        return self.output


class Report(MainBlock):
    def __init__(self, book: Path):
        self.book = book

    stat = StatBlock()
