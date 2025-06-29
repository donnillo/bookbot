import pathlib

type Path = str | pathlib.Path

SRC = pathlib.Path(__file__).parent
APP_NAME = SRC.stem
BOOKS = (SRC / "books").relative_to(SRC)
