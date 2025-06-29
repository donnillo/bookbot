from collections import defaultdict
from collections.abc import Callable
from collections.abc import Mapping
from operator import itemgetter

from paths import Path

type Counter = Mapping[str, int] | list[tuple[str, int]]


def word_count(path: Path, *, start: int = 0) -> int:
    with open(path, 'r') as book:
        for line in book.readlines():
            start += len(line.split())
    return start


def character_count(
    path: Path, *,
    transform: Callable[[str], str] | None = str.lower,
    sort: bool = False,
    ascending: bool = False,
    top: int | None = None,
) -> dict[str, int]:
    counter: Counter = defaultdict(int)
    with open(path, 'r') as book:
        for line in book.readlines():
            for char in (
                transform(line) if transform is not None else line
            ):
                counter[char] += 1
    if sort:
        counter = sorted(
            counter.items(), reverse=not ascending, key=itemgetter(1)
        )[slice(None, top)]
    return dict(counter)
