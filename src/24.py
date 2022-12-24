from typing import List, Set, Tuple

from utils import get_input

Coord = Tuple[int, int]
Blizzards = frozenset[Tuple[Coord, Coord]]


def parse_input(input: List[str]) -> Blizzards:
    # Disregard from the walls
    without_walls = input[1:-1]
    blizzards = set()
    for y, line in enumerate(without_walls):
        for x, char in enumerate(line[1:-1]):
            coord = (x, y)
            if char == "v":
                blizzards.add((coord, (0, 1)))
            if char == "^":
                blizzards.add((coord, (0, -1)))
            if char == ">":
                blizzards.add((coord, (1, 0)))
            if char == "<":
                blizzards.add((coord, (-1, 0)))
    return frozenset(blizzards)


def print_map(current: Coord, blizzards: Blizzards, max_x: int, max_y: int) -> None:
    print("Grid time")
    for y in range(max_y):
        line = ""
        for x in range(max_x):
            coord = (x, y)
            if current == coord:
                line += "E"
            elif (coord, (0, 1)) in blizzards:
                line += "v"
            elif (coord, (0, -1)) in blizzards:
                line += "^"
            elif (coord, (1, 0)) in blizzards:
                line += ">"
            elif (coord, (-1, 0)) in blizzards:
                line += "<"
            else:
                line += "."
        print(line)


def move_blizzards(blizzards: Blizzards, max_y: int, max_x: int) -> Blizzards:
    new_blizzards = frozenset(
        (((x + dx) % max_x, (y + dy) % max_y), (dx, dy))
        for ((x, y), (dx, dy)) in blizzards
    )
    return new_blizzards


def iterate(
    blizzards: Blizzards,
    goals: List[Coord],
    max_x: int,
    max_y: int,
) -> int:
    current_blizzards = blizzards
    rounds = 0
    new_next_positions: List[Coord] = [(0, -1)]
    next_pos: List[Coord] = []
    memo: Set[Tuple[Coord, Blizzards]] = set()
    current_goal = goals.pop(0)
    while True:
        # print(f"Round {rounds}")
        current_blizzards = move_blizzards(current_blizzards, max_y, max_x)
        blizzards_no_direction = set(blizzard[0] for blizzard in current_blizzards)
        next_pos = new_next_positions
        new_next_positions = []
        for (x, y) in next_pos:
            state = ((x, y), current_blizzards)
            if state in memo:
                continue
            memo.add(state)
            # Check if we the goal is below us
            if (x, y + 1) == current_goal or (x, y - 1) == current_goal:
                if len(goals) == 0:
                    return rounds + 1
                new_next_positions = [current_goal]
                current_goal = goals.pop(0)
                memo = set()
                break
            if y >= 0 and (x - 1) >= 0 and ((x - 1), y) not in blizzards_no_direction:
                # Move left
                new_next_positions.append((x - 1, y))
            if (
                y >= 0
                and (x + 1) < max_x
                and ((x + 1), y) not in blizzards_no_direction
            ):
                # Move right
                new_next_positions.append((x + 1, y))
            if y >= 0 and (y - 1) >= 0 and (x, y - 1) not in blizzards_no_direction:
                # Move up
                new_next_positions.append((x, y - 1))
            if (y + 1) < max_y and (x, y + 1) not in blizzards_no_direction:
                # Move down
                new_next_positions.append((x, y + 1))
            if (x, y) not in blizzards_no_direction:
                # Base case, do not move
                new_next_positions.append((x, y))
        rounds += 1


def main(input: List[str]) -> None:
    max_y = len(input) - 2
    max_x = len(input[0]) - 2
    blizzards = parse_input(input)
    print(f"Part 1: {iterate(blizzards, [(max_x - 1, max_y)], max_x, max_y)}")
    part2 = iterate(
        blizzards, [(max_x - 1, max_y), (0, -1), (max_x - 1, max_y)], max_x, max_y
    )
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main(get_input(24, False, strip=True))
