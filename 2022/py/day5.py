from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Generator, Generic, Iterable, NamedTuple, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    _deque: deque
    black_list: list

    def __init__(
        self, items: Iterable[T] | None = None, black_list: list | None = None
    ) -> None:
        self._deque = deque(items) if items else deque()
        self.black_list = black_list or []

    def __len__(self) -> int:
        return len(self._deque)

    # Part 2
    def __iadd__(self, other: Stack):
        self._deque += other._deque
        return self

    def __repr__(self) -> str:
        return f"Stack{repr(self._deque)[5:]}"

    # Part 2
    def partition(self, quantity) -> Stack[T]:
        """Slices off and returns a new stack composed of the top `n` items."""
        partitioned_items = [self._deque.pop() for _ in range(quantity)]
        return Stack(reversed(partitioned_items))

    def append(self, item: T):
        self._deque.append(item)

    def add(self, item: T):
        if item in self.black_list:
            raise ValueError(f"{item} is on `black_list` - {self.black_list}")
        self.append(item)

    def pop(self) -> T:
        try:
            return self._deque.pop()
        except IndexError as empty_exc:
            raise IndexError("Stack is empty") from empty_exc

    @classmethod
    def _parse_line(cls, line: str) -> list[str]:
        return list(line[1::4])

    @classmethod
    def from_2d_array(
        cls, array: list[list[T]], black_list: list | None = None
    ) -> list[Stack[T]]:
        black_list = black_list or []
        stacks = [cls(black_list=black_list) for _ in range(len(array[0]))]

        # starting from bottom row
        for row in array[::-1]:
            for idx, item in enumerate(row):
                if item not in black_list:
                    stacks[idx].add(item)
        return stacks

    @classmethod
    def from_diagram(cls, diagram_txt: str) -> list[Stack[str]]:
        _2d_array = [cls._parse_line(ls) for ls in diagram_txt.splitlines()]
        return cls.from_2d_array(
            _2d_array,
            black_list=[" "],  # type: ignore[arg-type,return-value]
        )


class Instruction(NamedTuple):
    quantity: int
    source_idx: int
    target_idx: int

    @classmethod
    def parse_line(cls, line: str) -> Instruction:
        _, q, _, s, _, t = line.split(" ")
        return cls(int(q), int(s), int(t))


KT = TypeVar("KT", bound=int)
VT = TypeVar("VT", bound=Stack)


class CargoShip(Generic[KT, VT]):
    cargo: list[VT]

    @property
    def total_cargo(self):
        return sum(len(c) for c in self.cargo)

    def __init__(self, cargo: list[VT] | None = None):
        self.cargo = cargo or []

    def __len__(self) -> int:
        return len(self.cargo)

    def __repr__(self) -> str:
        return f"{type(self).__name__} |{'|'.join([str(len(c)) for c in self.cargo])}|"

    def __getitem__(self, idx: KT) -> VT:
        adjusted_idx = idx - 1
        num_cargo = len(self)
        if not idx or idx > num_cargo:
            raise IndexError(f"Incompatible `idx` {idx} expected 1 - {num_cargo}")
        return self.cargo[adjusted_idx]

    def move_cargo(self, source_idx: int, target_idx: int, quantity: int = 1):
        for _ in range(quantity):
            source_stack = self[source_idx]  # type: ignore[index]
            target_stack = self[target_idx]  # type: ignore[index]

            item = source_stack.pop()
            target_stack.add(item)

    def process_instruction(self, instruction: Instruction):
        initial_cargo = self.total_cargo
        self.move_cargo(
            instruction.source_idx, instruction.target_idx, instruction.quantity
        )
        assert self.total_cargo == initial_cargo


def extract_initial_cargo_stacks(input_file: Path) -> list[Stack]:
    starting_stacks: list[str] = []
    with open(input_file) as f_in:
        while True:
            line = next(f_in)
            if line == "\n":  # starting stacks section ends
                starting_stacks = starting_stacks[:-1]  # remove the unneeded stack labels
                return Stack.from_diagram("".join(starting_stacks))
            starting_stacks.append(line)


def extract_instructions(input_file: Path) -> Generator[Instruction, None, None]:
    with open(input_file) as f_in:
        line = next(f_in)
        while not line.startswith("\n"):
            line = next(f_in)
        while True:
            try:
                line = next(f_in)
                yield Instruction.parse_line(line)
            except StopIteration:
                break


def run_excercise(
    initial_stacks: list[Stack],
    ship_class: type[CargoShip],
    instructions: Iterable[Instruction],
):
    ship = ship_class(initial_stacks)
    print(f"Initial state\n{ship}")
    ship.cargo

    # start at 11 to match text file line numbers
    for i, instr in enumerate(instructions, start=11):
        try:
            ship.process_instruction(instr)
        except IndexError as err:
            print(f"{instr} {i=} {err}")

    print(f"\nFinal state\n{ship}")
    ship.cargo

    top_items: list[str] = [s.pop() for s in ship.cargo]
    print("".join(top_items))


# Part 2


class CrateMover9001(CargoShip):
    def move_cargo(self, source_idx: int, target_idx: int, quantity: int = 1):
        source_stack = self[source_idx]  # type: ignore[index]
        target_stack = self[target_idx]  # type: ignore[index]

        in_trasit_stack = source_stack.partition(quantity)
        target_stack += in_trasit_stack


if __name__ == "__main__":
    from codetiming import Timer

    input_file = Path(__file__).joinpath("..", "..", "inputs", "day5.txt").resolve()
    assert input_file.exists(), input_file

    with Timer():
        print("\n  Part One")
        initial_stacks = extract_initial_cargo_stacks(input_file)
        instructions = extract_instructions(input_file)
        run_excercise(initial_stacks, CargoShip, instructions)

    with Timer():
        print("\n  Part Two")
        initial_stacks = extract_initial_cargo_stacks(input_file)
        instructions = extract_instructions(input_file)
        run_excercise(initial_stacks, CrateMover9001, instructions)
