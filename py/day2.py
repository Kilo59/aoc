from __future__ import annotations

import enum
import functools
from pathlib import Path
from typing import Callable, ClassVar, Generator, Iterator, TypeAlias


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

    def __hash__(self) -> int:
        """Return ASCII code of the first character."""
        # Needed for lru & set operations in part 2
        return ord(self.__class__.__name__[0])


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


def rps_factory_1(char: str) -> Rock | Paper | Scissors:
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


def ingest_rps_picks_1(
    input_file: Path,
) -> Generator[tuple[Rock | Paper | Scissors, Rock | Paper | Scissors], None, None]:
    with open(input_file) as f_in:
        for line in f_in:
            opponent_pick, my_pick = line.split()
            yield rps_factory_1(opponent_pick), rps_factory_1(my_pick)


def play_games(
    input_file: Path,
    rps_picks_iter: Callable[
        [Path], Iterator[tuple[Rock | Paper | Scissors, Rock | Paper | Scissors]]
    ],
):
    WIN: int = 6
    DRAW: int = 3
    LOSS: int = 0

    my_score: int = 0
    opp_score: int = 0
    rounds_played: int = 0

    for opp_pick, my_pick in rps_picks_iter(input_file):
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

    print(f"Rounds - {rounds_played}\n{my_score=}\n{opp_score=}\n")


# Part 2


class OpponentPick(str, enum.Enum):
    ROCK = "A"
    PAPER = "B"
    SCISSORS = "C"


class MyStrategy(str, enum.Enum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"


RPS: TypeAlias = Rock | Paper | Scissors


@functools.lru_cache(maxsize=32)
def _select_rps_for_strategy(opp_rps: RPS, my_strat: MyStrategy) -> RPS:
    options: set[RPS] = {Rock(), Paper(), Scissors()}

    if my_strat == MyStrategy.DRAW:
        return opp_rps
    options.remove(opp_rps)  # only needed for draw

    for choice in options:
        if my_strat == MyStrategy.WIN and choice > opp_rps:
            return choice
        if my_strat == MyStrategy.LOSE and choice < opp_rps:
            return choice

    raise NotImplementedError("Don't know how to satisfy strategy")


def rps_factory_2(opp_pick: OpponentPick, my_strat: MyStrategy) -> tuple[RPS, RPS]:
    pick_mapping: dict[str, RPS] = {
        OpponentPick.ROCK: Rock(),
        OpponentPick.PAPER: Paper(),
        OpponentPick.SCISSORS: Scissors(),
    }

    opp_rps_pick: RPS = pick_mapping[opp_pick]

    my_rps_pick: RPS = _select_rps_for_strategy(opp_rps_pick, my_strat)

    return opp_rps_pick, my_rps_pick


def ingest_rps_picks_2(
    input_file: Path,
) -> Generator[tuple[Rock | Paper | Scissors, Rock | Paper | Scissors], None, None]:
    with open(input_file) as f_in:
        for line in f_in:
            opponent_pick, my_strat = line.split()
            yield rps_factory_2(opponent_pick, my_strat)  # type: ignore[arg-type]


if __name__ == "__main__":
    input_file = Path(__file__).joinpath("..", "..", "inputs", "day2.txt").resolve()
    assert input_file.exists(), input_file

    print("Part 1")
    play_games(input_file, ingest_rps_picks_1)

    print("Part 2")
    play_games(input_file, ingest_rps_picks_2)
