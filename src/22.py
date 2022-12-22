import math
import re
from typing import Dict, List, Set, Tuple

from utils import get_input

Coord = Tuple[int, int]
Instruction = int | str
Regions = Dict[int, Tuple[Set[Coord], Coord]]

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
    monkey: Coord,
    direction: Coord,
    times: int,
    free: Set[Coord],
    blocked: Set[Coord],
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


def next_coord(
    monkey: Coord, direction: Coord, regions: Regions, region_size: int
) -> Tuple[Coord, Coord]:
    region_offset = region_size - 1
    normalized_x = monkey[0] % region_size
    normalized_y = monkey[1] % region_size
    # Dirty solution, calculated by hand
    if monkey in regions[1][0]:
        if direction == (-1, 0):
            start_x, start_y = regions[4][1]
            # Wraps to 4 left side, y coords gets flipped
            return (start_x, start_y + region_offset - normalized_y), (1, 0)
        if direction == (0, -1):
            start_x, start_y = regions[6][1]
            # Wraps to 6 left side
            return (start_x, start_y + normalized_x), (1, 0)
    if monkey in regions[2][0]:
        if direction == (0, -1):
            start_x, start_y = regions[6][1]
            # Wraps to 6 bottom side
            return (start_x + normalized_x, start_y + region_offset), (0, -1)
        if direction == (1, 0):
            start_x, start_y = regions[5][1]
            # Wraps to 5 right side
            return (start_x + region_offset, start_y + region_offset - normalized_y), (
                -1,
                0,
            )
        if direction == (0, 1):
            start_x, start_y = regions[3][1]
            # Wraps to 3 right side
            return (start_x + region_offset, start_y + normalized_x), (-1, 0)
    if monkey in regions[3][0]:
        if direction == (1, 0):
            start_x, start_y = regions[2][1]
            # Wraps to 2 bottom side
            return (start_x + normalized_y, start_y + region_offset), (0, -1)
        if direction == (-1, 0):
            # Wraps to 4 top side
            start_x, start_y = regions[4][1]
            return (start_x + normalized_y, start_y), (0, 1)
    if monkey in regions[4][0]:
        if direction == (0, -1):
            start_x, start_y = regions[3][1]
            # Wraps to 3 left side
            return (start_x, start_y + normalized_x), (1, 0)
        if direction == (-1, 0):
            # Wraps to 1 left side
            start_x, start_y = regions[1][1]
            return (start_x, start_y + region_offset - normalized_y), (1, 0)
    if monkey in regions[5][0]:
        if direction == (1, 0):
            start_x, start_y = regions[2][1]
            # Wraps to 2 right side
            return (start_x + region_offset, start_y + region_offset - normalized_y), (
                -1,
                0,
            )
        if direction == (0, 1):
            # Wraps to 6 right side
            start_x, start_y = regions[6][1]
            return (start_x + region_offset, start_y + normalized_x), (-1, 0)
    if monkey in regions[6][0]:
        if direction == (-1, 0):
            start_x, start_y = regions[1][1]
            # Wraps to 1 top side
            return (start_x + normalized_y, start_y), (0, 1)
        if direction == (0, 1):
            # Wraps to 2 top side
            start_x, start_y = regions[2][1]
            return (start_x + normalized_x, start_y), (0, 1)
        if direction == (1, 0):
            # Wraps to 5 bottom side
            start_x, start_y = regions[5][1]
            return (start_x + normalized_y, start_y + region_offset), (0, -1)
    print(monkey)
    print(direction)
    raise Exception("Should not happen")


def move_monkey2(
    monkey: Coord,
    direction: Coord,
    times: int,
    free: Set[Coord],
    blocked: Set[Coord],
    regions: Regions,
    region_size: int,
) -> Tuple[Coord, Coord]:
    current_monkey = monkey
    current_direction = direction
    for _ in range(times):
        next_monkey = (
            current_monkey[0] + current_direction[0],
            current_monkey[1] + current_direction[1],
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
        next_monkey, next_direction = next_coord(
            current_monkey, current_direction, regions, region_size
        )
        if next_monkey in blocked:
            break
        current_monkey = next_monkey
        current_direction = next_direction
    return current_monkey, current_direction


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
    start = sorted(top_row, key=lambda a: a[0])[0]  # Lowest y with the lowest x
    monkey = start
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
    print(f"Part 1: {part1}")
    # Divide grid into parts 1-6
    # Determine size of each region
    # Size = region_size ^ 2
    all_points = free.union(blocked)
    region_size = int(math.sqrt((len(all_points)) // 6))
    current_region = 1
    regions: Regions = {}
    for y_i in range(0, max_y, region_size):
        for x_i in range(0, max_x, region_size):
            if (x_i, y_i) in all_points:
                regions[current_region] = (
                    set(
                        (x, y)
                        for x, y in all_points
                        if x >= x_i
                        and x < x_i + region_size
                        and y >= y_i
                        and y < y_i + region_size
                    ),
                    (x_i, y_i),
                )
                current_region += 1
    monkey = start
    direction = (1, 0)
    for instruction in instructions:
        if isinstance(instruction, int):
            monkey, direction = move_monkey2(
                monkey, direction, instruction, free, blocked, regions, region_size
            )
            continue
        # Turn
        direction = turn(direction, instruction)
    part2 = (
        ((monkey[0] + 1) * 4) + ((monkey[1] + 1) * 1000) + direction_score[direction]
    )
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main(get_input(22, False, strip=False))
