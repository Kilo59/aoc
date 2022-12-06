from collections import deque
from pathlib import Path
from typing import NamedTuple


class MarkerDetails(NamedTuple):
    marker: str
    position: int


def find_marker(buffer: str, marker_length: int = 4) -> MarkerDetails:
    possible_marker: deque[str] = deque(maxlen=marker_length)
    for i, c in enumerate(buffer):

        if len(set(possible_marker)) == marker_length:
            marker = buffer[i - marker_length : i]
            print(f"Marker found after {i} - {marker}")
            return MarkerDetails(marker=marker, position=i)

        possible_marker.append(c)
    raise ValueError("No marker found in buffer")


if __name__ == "__main__":
    BUFFER = Path(__file__).parent.parent.joinpath("inputs", "day6.txt").read_text()

    # Part One
    find_marker(BUFFER, marker_length=4)

    # Part Two
    find_marker(BUFFER, marker_length=14)
