import re
from typing import List, Set, Tuple

from utils import get_input

Coord = Tuple[int, int]
Instruction = Tuple[int, str]

instruction_re = r"(\d+)(R|L)"


def parse_input(input: List[str]) -> Tuple[Set[Coord], Set[Coord], List[Instruction]]:
    free = set()
    blocked = set()
    last_line = input[-1]
    for y, line in enumerate(input[:-1]):
        for x, char in enumerate(line):
            if char == ".":
                free.add((x, y))
            elif char == "#":
                blocked.add((x, y))
    instructions_match = [
        (int(num), dir) for num, dir in re.findall(instruction_re, last_line)
    ]
    return free, blocked, instructions_match


def main(input: List[str]) -> None:
    free, blocked, instructuions = parse_input(input)
    min_y = min(y for _, y in free)
    top_row = ((x, y) for x, y in free if y == min_y)
    start = sorted(top_row, key=lambda a: a[0])[0]  # Lowest y with the lowest x
    print(start)


if __name__ == "__main__":
    main(get_input(22, True, strip=False))
