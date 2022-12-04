from pathlib import Path
from typing import Callable, Generator


def range_from_str(s: str) -> range:
    i1, i2 = s.split("-")
    return range(int(i1), int(i2))


def ingest_range_pairs(input_file: Path) -> Generator[tuple[range, range], None, None]:
    with open(input_file) as f_in:
        for line in f_in:
            s1, s2 = line.rstrip().split(",")
            yield range_from_str(s1), range_from_str(s2)


def full_overlap(r1: range, r2: range) -> bool:
    if r1.start >= r2.start and r1.stop <= r2.stop:
        return True
    return r2.start >= r1.start and r2.stop <= r1.stop


def partial_overlap(r1: range, r2: range) -> bool:
    r1_set = set(r1)
    r2_set = set(r2)
    for range_, set_ in zip((r1, r2), (r1_set, r2_set)):
        set_.add(range_.stop)  # end of range should be included

    return bool(r1_set.intersection(r2_set))


def check_overlapping_pairs(
    input_file: Path, is_overlap_check: Callable[[range, range], bool]
):
    overlap_count = sum(
        1
        for pairs in ingest_range_pairs(input_file)
        if is_overlap_check(*pairs)
    )

    print(f"{overlap_count=}")


if __name__ == "__main__":
    from codetiming import Timer

    input_file = Path(__file__).joinpath("..", "..", "inputs", "day4.txt").resolve()
    assert input_file.exists(), input_file

    with Timer("1"):
        print("\nPart One")
        check_overlapping_pairs(input_file, is_overlap_check=full_overlap)

    with Timer("2"):
        print("\nPart Two")
        check_overlapping_pairs(input_file, is_overlap_check=partial_overlap)
