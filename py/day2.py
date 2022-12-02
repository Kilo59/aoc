from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Generator


class RPSBase:
    score: ClassVar[int]

    @property
    def beats(self) -> type[RPSBase]:
        # can't define this as a class level attribute, classes hasn't been defined yet
        raise NotImplementedError(
            f"{self.__class__.__name__} must return the class it beats"
        )

    def __gt__(self, other: RPSBase) -> bool:
        return isinstance(other, self.beats)

    def __eq__(self, other: object) -> bool:
        return self.__class__ == other.__class__


class Rock(RPSBase):
    score = 1

    @property
    def beats(self):
        return Scissors


class Paper(RPSBase):
    score = 2

    @property
    def beats(self):
        return Rock


class Scissors(RPSBase):
    score = 3

    @property
    def beats(self):
        return Paper


def rps_factory(char: str) -> Rock | Paper | Scissors:
    # TODO: pattern matching?
    class_mapping: dict[str, type[Rock] | type[Paper] | type[Scissors]] = {
        "A": Rock,
        "X": Rock,
        "B": Paper,
        "Y": Paper,
        "C": Scissors,
        "Z": Scissors,
    }
    item_class = class_mapping[char]
    return item_class()


def ingest_rps_picks(
    input_file: Path,
) -> Generator[tuple[Rock | Paper | Scissors, Rock | Paper | Scissors], None, None]:
    with open(input_file) as f_in:
        for line in f_in:
            opponent_pick, my_pick = line.split()
            yield rps_factory(opponent_pick), rps_factory(my_pick)


if __name__ == "__main__":
    input_file = Path(__file__).joinpath("..", "..", "inputs", "day2.txt").resolve()
    assert input_file.exists(), input_file

    WIN: int = 6
    DRAW: int = 3
    LOSS: int = 0

    my_score: int = 0
    opp_score: int = 0
    rounds_played: int = 0

    for opp_pick, my_pick in ingest_rps_picks(input_file):
        my_score += my_pick.score
        opp_score += opp_pick.score

        if my_pick == opp_pick:
            my_score += DRAW
            opp_score += DRAW
        elif my_pick > opp_pick:
            my_score += WIN
            opp_score += LOSS
        elif opp_pick > my_pick:
            my_score += LOSS
            opp_score += WIN
        else:
            raise NotImplementedError("Unknown Condition Encountered")
        rounds_played += 1

    print(f"Rounds - {rounds_played}\n{my_score=}\n{opp_score=}")
