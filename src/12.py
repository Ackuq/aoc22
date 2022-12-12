from typing import Dict, List, Tuple

from utils import get_input

Coord = Tuple[int, int]
Grid = List[List[int]]


def parse_input(input: List[str]) -> Tuple[Grid, Coord, Coord]:
    start: Coord
    end: Coord
    grid: Grid = []
    for y, line in enumerate(input):
        row: List[int] = []
        for x, col in enumerate(line):
            if col.islower():
                row.append(ord(col) - 97)
                continue
            elif col == "S":
                start = (x, y)
                row.append(0)
            elif col == "E":
                end = (x, y)
                row.append(25)
        grid.append(row)

    return (
        grid,
        start,
        end,
    )


def valid_move(grid: Grid, coord1: Coord, coord2: Coord) -> bool:
    diff = grid[coord2[1]][coord2[0]] - grid[coord1[1]][coord1[0]]
    return diff <= 1


def get_neighbors(grid: Grid, coord: Coord) -> List[Coord]:
    neighbors: List[Coord] = []
    x, y = coord
    if x > 0 and valid_move(grid, coord, (x - 1, y)):
        neighbors.append((x - 1, y))
    if y > 0 and valid_move(grid, coord, (x, y - 1)):
        neighbors.append((x, y - 1))
    if y < len(grid) - 1 and valid_move(grid, coord, (x, y + 1)):
        neighbors.append((x, y + 1))
    if x < len(grid[0]) - 1 and valid_move(grid, coord, (x + 1, y)):
        neighbors.append((x + 1, y))
    return neighbors


def djikstra(grid: Grid, start: Coord, end: Coord) -> int:
    queue: List[Coord] = []
    dists: Dict[Coord, int] = {}
    pred: Dict[Coord, Coord] = {}
    visited: Dict[Coord, bool] = {}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            coord = (x, y)
            dists[coord] = 100_000_000
            pred[coord] = (-1, -1)
            visited[coord] = False
    visited[start] = True
    dists[start] = 0
    queue.append(start)

    while len(queue) > 0:
        current = queue.pop(0)
        for neighbor in get_neighbors(grid, current):
            if not visited[neighbor]:
                visited[neighbor] = True
                dists[neighbor] = dists[current] + 1
                pred[neighbor] = current
                queue.append(neighbor)
                if neighbor == end:
                    return dists[neighbor]
    return -1


def main(input: List[str]) -> None:
    grid, start, end = parse_input(input)
    part1 = djikstra(grid, start, end)
    print(f"Part 1 {part1}")
    possible_starts: List[Coord] = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == 0 and (x, y) != start:
                possible_starts.append((x, y))

    minimum = part1
    for possible_start in possible_starts:
        val = djikstra(grid, possible_start, end)
        if val < minimum and val != -1:
            minimum = val

    print(f"Part 2 {minimum}")


if __name__ == "__main__":
    main(get_input(12, False, strip=True))
