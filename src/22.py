import re
from typing import Dict, List, Set, Tuple

from utils import get_input

Coord = Tuple[int, int]
Instruction = int | str

instruction_re = r"(\d+|R|L)"


def parse_input(
    input: List[str],
) -> Tuple[Set[Coord], Set[Coord], List[Instruction], int, int]:
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
        int(instr) if instr.isnumeric() else instr
        for instr in re.findall(instruction_re, last_line)
    ]
    max_y = len(input) - 2
    max_x = max(len(line) for line in input[:-2])
    return free, blocked, instructions_match, max_x, max_y


def turn(current: Coord, direction: str) -> Coord:
    if direction == "R":
        return (-current[1], current[0])
    return (current[1], -current[0])


def move_monkey(
    monkey: Coord, direction: Coord, times: int, free: Set[Coord], blocked: Set[Coord]
) -> Coord:
    current_monkey = monkey
    for _ in range(times):
        next_monkey = (
            current_monkey[0] + direction[0],
            current_monkey[1] + direction[1],
        )
        if next_monkey in free:
            # Move forwards
            current_monkey = next_monkey
            continue
        if next_monkey in blocked:
            # Break
            break
        # Else we must wrap, move opposite of current direction until last is
        # found
        next_monkey = (
            current_monkey[0] - direction[0],
            current_monkey[1] - direction[1],
        )
        while True:
            possible_next_monkey = (
                next_monkey[0] - direction[0],
                next_monkey[1] - direction[1],
            )
            if possible_next_monkey not in free and possible_next_monkey not in blocked:
                # This is the edge, check if we are blocked
                if next_monkey in blocked:
                    return current_monkey
                current_monkey = next_monkey
                break
            next_monkey = possible_next_monkey
    return current_monkey


def print_grid(
    monkey: Coord,
    direction: Coord,
    free: Set[Coord],
    blocked: Set[Coord],
    max_x: int,
    max_y: int,
) -> None:
    print("Grid time")
    for y in range(max_y):
        line = ""
        for x in range(max_x):
            coord = (x, y)
            if coord == monkey:
                if direction == (1, 0):
                    line += ">"
                if direction == (0, 1):
                    line += "v"
                if direction == (-1, 0):
                    line += "<"
                if direction == (0, -1):
                    line += "^"
                continue
            if coord in free:
                line += "."
                continue
            if coord in blocked:
                line += "#"
                continue
            line += " "
        print(line)


direction_score: Dict[Coord, int] = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3,
}


def main(input: List[str]) -> None:
    free, blocked, instructions, max_x, max_y = parse_input(input)
    min_y = min(y for _, y in free)
    top_row = ((x, y) for x, y in free if y == min_y)
    monkey = sorted(top_row, key=lambda a: a[0])[0]  # Lowest y with the lowest x
    direction = (1, 0)
    for instruction in instructions:
        # print_grid(monkey, direction, free, blocked, max_x, max_y)
        if isinstance(instruction, int):
            monkey = move_monkey(monkey, direction, instruction, free, blocked)
            continue
        # Turn
        direction = turn(direction, instruction)
    part1 = (
        ((monkey[0] + 1) * 4) + ((monkey[1] + 1) * 1000) + direction_score[direction]
    )
    print(f"Part 1 {part1}")


if __name__ == "__main__":
    main(get_input(22, False, strip=False))
