import math
from typing import List, Tuple

from utils import get_input

Grid = List[List[int]]


def to_grid(input: List[str]) -> Grid:
    return [[int(char) for char in line] for line in input]


def is_visible(grid: Grid, value: int, coordinates: Tuple[int, int]) -> bool:
    x, y = coordinates
    for y_1 in range(y - 1, -1, -1):
        # Check y positive
        if grid[y_1][x] >= value:
            break
        if y_1 == 0:
            return True
    for y_1 in range(y + 1, len(grid)):
        if grid[y_1][x] >= value:
            break
        if y_1 == len(grid) - 1:
            return True
    for x_1 in range(x - 1, -1, -1):
        if grid[y][x_1] >= value:
            break
        if x_1 == 0:
            return True
    for x_1 in range(x + 1, len(grid[y])):
        if grid[y][x_1] >= value:
            break
        if x_1 == len(grid[y]) - 1:
            return True
    return False


def visible_trees(grid: Grid, value: int, coordinates: Tuple[int, int]) -> int:
    x, y = coordinates
    scores = [0, 0, 0, 0]
    for y_1 in range(y - 1, -1, -1):
        scores[0] += 1
        if grid[y_1][x] >= value:
            break
    for y_1 in range(y + 1, len(grid)):
        scores[1] += 1
        if grid[y_1][x] >= value:
            break
    for x_1 in range(x - 1, -1, -1):
        scores[2] += 1
        if grid[y][x_1] >= value:
            break
    for x_1 in range(x + 1, len(grid[y])):
        scores[3] += 1
        if grid[y][x_1] >= value:
            break
    return math.prod(scores)


def main(input: List[str]) -> None:
    grid = to_grid(input)
    outer = len(grid) * 2 + len(grid[0]) * 2 - 4
    not_visible: List[Tuple[int, int]] = []
    inner = 0
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            if is_visible(grid, grid[y][x], (x, y)):
                inner += 1
            else:
                not_visible.append((x, y))
    print(f"Part 1: {inner + outer}")
    max_visible = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            visible = visible_trees(grid, grid[y][x], (x, y))
            if visible > max_visible:
                max_visible = visible

    print(f"Part 2: {max_visible}")


if __name__ == "__main__":
    main(get_input(8, False, strip=True))
