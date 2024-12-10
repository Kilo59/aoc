from collections.abc import Generator
from pathlib import Path
from queue import PriorityQueue


def ingest_inventory_sums(input_file: Path) -> Generator[int, None, None]:
    assert input_file.exists(), f"{input_file} does not exist"

    current_elf: list[int] = []

    with open(input_file) as f_in:
        for line in f_in:
            # check for blank line indicating another elf's inventory
            if line.startswith("\n"):
                yield sum(current_elf)
                current_elf.clear()
                continue

            current_elf.append(int(line))


class OrderedQueue(PriorityQueue):
    """A priority queue that returns the highest value in the queue."""

    def put(self, item: int, block: bool = True, timeout: float | None = None):
        """
        Invert the sign of the added item so that higher numbers have highest priority.
        """
        return super().put(-item, block=block, timeout=timeout)

    def get(self, block: bool = True, timeout: float | None = None) -> int:
        """Revert the sign of retrieved item."""
        return -super().get(block=block, timeout=timeout)


if __name__ == "__main__":
    # Part 1

    input_file = Path(__file__).joinpath("..", "..", "inputs", "day1.txt").resolve()

    max_ = 0

    for elf_no, calorie_sum in enumerate(ingest_inventory_sums(input_file), start=1):
        if calorie_sum >= max_:
            max_ = calorie_sum
            print(f"New leader - Elf {elf_no} - {max_} kCal")
    print(f"Final Leader: {max_}\n")

    # Part 2

    top_q: OrderedQueue = OrderedQueue()

    for cal_sum in ingest_inventory_sums(input_file):
        top_q.put(cal_sum)

    top_cals: list[int] = []
    for _ in range(3):
        value = top_q.get()
        top_cals.append(value)

    print(top_cals)
    print(f"Top Elf sum: {sum(top_cals)}")
