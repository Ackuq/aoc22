import sys
from itertools import chain
from typing import Dict, List, Set, Tuple

from utils import get_input

Coord = Tuple[int, int]

Elves = Set[Coord]

Transitions = Dict[Coord, Coord]


def parse_input(input: List[str]) -> Elves:
    elves: Elves = set()
    for y, line in enumerate(reversed(input)):
        for x, char in enumerate(line):
            if char == "#":
                elves.add((x, y))
    return elves


def print_elves(elves: Elves, round: int) -> None:
    all_x = [x for x, _ in elves]
    all_y = [y for _, y in elves]
    print(f"=== End of round {round} ===")
    for y in range(max(all_y), min(all_y) - 1, -1):
        line = ""
        for x in range(min(all_x), max(all_x) + 1):
            if (x, y) in elves:
                line += "#"
                continue
            line += "."
        print(line)


def next_coord(coord: Coord, elves: Elves, order: List[str]) -> Coord:
    # Check N, NW and NE
    # If no elf in any adjacent
    x, y = coord
    if (
        (x - 1, y - 1) not in elves
        and (x - 1, y) not in elves
        and (x - 1, y + 1) not in elves
        and (x, y + 1) not in elves
        and (x, y - 1) not in elves
        and (x + 1, y + 1) not in elves
        and (x + 1, y) not in elves
        and (x + 1, y - 1) not in elves
    ):
        return coord
    for dir in order:
        if (
            dir == "N"
            and (x - 1, y + 1) not in elves
            and (x, y + 1) not in elves
            and (x + 1, y + 1) not in elves
        ):
            return (x, y + 1)
        # Check S, SW, SE
        if (
            dir == "S"
            and (x - 1, y - 1) not in elves
            and (x, y - 1) not in elves
            and (x + 1, y - 1) not in elves
        ):
            return (x, y - 1)
        # Check W, NW, SW
        if (
            dir == "W"
            and (x - 1, y - 1) not in elves
            and (x - 1, y) not in elves
            and (x - 1, y + 1) not in elves
        ):
            return (x - 1, y)
        # Check E, NE, SE
        if (
            dir == "E"
            and (x + 1, y - 1) not in elves
            and (x + 1, y) not in elves
            and (x + 1, y + 1) not in elves
        ):
            return (x + 1, y)
    return coord


def get_empty(elves: Elves) -> int:
    empty = 0
    all_x = [x for x, _ in elves]
    all_y = [y for _, y in elves]
    for y in range(min(all_y), max(all_y) + 1):
        for x in range(min(all_x), max(all_x) + 1):
            if (x, y) not in elves:
                empty += 1
    return empty


def run(input: List[str], times: int = sys.maxsize, part2: bool = False) -> int:
    elves = parse_input(input)
    order = ["N", "S", "W", "E"]
    for round in range(times):
        transitions: Transitions = {}
        for elf in elves:
            next_move = next_coord(elf, elves, order)
            transitions[elf] = next_move

        # Move direction order dict
        first = order.pop(0)
        order.append(first)
        # Get all duplicates
        reversed_dict: Dict[Coord, Set[Coord]] = {}
        for key, value in transitions.items():
            reversed_dict.setdefault(value, set()).add(key)

        keys_with_duplicates = set(
            chain.from_iterable(
                values for _, values in reversed_dict.items() if len(values) > 1
            )
        )
        for key in keys_with_duplicates:
            # Make these not move
            transitions[key] = key
        if part2 and all(key == value for key, value in transitions.items()):
            return round + 1
        elves = set(transitions.values())
        # print_elves(elves, i + 1)
    return get_empty(elves)


def main(input: List[str]) -> None:
    print(f"Part 1: {run(input, 10)}")
    print(f"Part 2: {run(input, part2=True)}")


if __name__ == "__main__":
    main(get_input(23, strip=True))
