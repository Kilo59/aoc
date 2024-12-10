import string
from collections.abc import Generator, Iterable
from pathlib import Path

PRIORITY_LOOKUP: dict[str, int] = {
    c: i for i, c in enumerate(string.ascii_letters, start=1)
}


# Part 1


def bisect_string(s: str) -> tuple[str, str]:
    s = s.rstrip()
    return s[: len(s) // 2], s[len(s) // 2 :]


def ingest_items(input_file: Path) -> Generator[tuple[str, str], None, None]:
    with open(input_file) as f_in:
        for line in f_in:
            yield bisect_string(line)


def find_common_character(collections: tuple[str, str]) -> str:
    s1, s2 = collections
    return "".join({c for c in s1 if c in s2})


# Part 2


def grouper(iterable: Iterable[str], n: int) -> Iterable[tuple[str, ...]]:
    """ "
    Collect data into non-overlapping fixed-length chunks or blocks

    Example
        grouper('ABCDEFGHI', 3) --> ABC DEF GHI
    """
    # simplified itertools recipe
    # https://docs.python.org/3/library/itertools.html#itertools-recipes
    args = [iter(iterable)] * n
    return zip(*args, strict=True)


def ingest_items_2(input_file: Path) -> Generator[tuple[str, str, str], None, None]:
    with open(input_file) as f_in:
        for item in grouper(f_in, 3):
            yield tuple(x.rstrip() for x in item)  # type: ignore[misc]


def find_common_item(group: tuple[str, str, str]) -> str:
    e1, e2, e3 = group
    for c in e1:
        if c in e2 and c in e3:
            return c
    raise LookupError("No common items")


if __name__ == "__main__":
    from codetiming import Timer

    input_file = Path(__file__).joinpath("..", "..", "inputs", "day3.txt").resolve()
    assert input_file.exists(), input_file

    with Timer("Part One"):
        priority_scores = [
            PRIORITY_LOOKUP[find_common_character(x)] for x in ingest_items(input_file)
        ]

        priority_sum = sum(priority_scores)
        print(f"\nPart One\n{priority_sum=}")

    with Timer("Part Two"):
        badge_priority_scores = [
            PRIORITY_LOOKUP[find_common_item(group)]
            for group in ingest_items_2(input_file)
        ]

        badge_priority_sum = sum(badge_priority_scores)
        print(f"\nPart Two\n{badge_priority_sum=}")
