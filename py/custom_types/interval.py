from __future__ import annotations

# TODO: add & subtract intervals
# TODO: re-calculate range, set from start, stop (or make immutable)


class Interval:
    _start: int
    _stop: int
    _range: range
    _set: set[int]

    def __init__(self, interval: str):
        if not isinstance(interval, str):
            raise TypeError(
                f"Expected interval string in the format '1-99', got {type(interval)}"
            )

        start, stop = interval.split("-")
        self._start = int(start)
        self._stop = int(stop)
        self._range = range(self._start, self._stop + 1)
        self._set = set(self._range)

    def __repr__(self) -> str:
        return f"Interval({self._start}, {self._stop})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._start == other._start and self._stop == other._stop

    def __contains__(self, other) -> bool:
        return self._set.issuperset(set(other))

    def __iter__(self):
        for i in self._range:
            yield i

    def intersection(self, other) -> set[int]:  # type: ignore[valid-type]
        return self._set.intersection(set(other))


if __name__ == "__main__":
    a = Interval("1-10")
    b = Interval("2-8")
    A = Interval("1-10")
    c = Interval("11-20")

    assert a == A
    assert a != object()
    assert a != b
    assert b in a
    assert c not in a
    assert [1, 2] in a
