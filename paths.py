import sys
import pathlib

type Path = str | pathlib.Path

SRC = pathlib.Path(__file__).parent
APP_NAME = SRC.stem
BOOKS = (SRC / "books").relative_to(SRC)


def get_book_from_args() -> Path | None:
    if len(sys.argv) == 2:
        path = pathlib.Path(sys.argv[1])
        if path.parent == BOOKS:
            return path.name
        else:
            return path
