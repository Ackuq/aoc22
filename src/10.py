from typing import List, Tuple

from utils import get_input

CYCLES = [20, 60, 100, 140, 180, 220]


def tick(cycle: int, register: int, strengths: List[int]) -> Tuple[int, List[int]]:
    if cycle in CYCLES:
        strengths.append(cycle * register)
    return cycle + 1, strengths


def tick2(
    cycle: int, register: int, grid: List[List[str]]
) -> Tuple[int, List[List[str]]]:
    y = (cycle - 1) // 40
    x = (cycle - 1) % 40
    if x in range(register - 1, register + 2):
        grid[y][x] = "#"
    return cycle + 1, grid


def print_grid(grid: List[List[str]]) -> None:
    for row in grid:
        print("".join(row))


def main(input: List[str]) -> None:
    cycle = 1
    register = 1
    strengths: List[int] = []
    for line in input:
        if line == "noop":
            cycle, signal_strength = tick(cycle, register, strengths)
        elif line.startswith("addx"):
            value = int(line.split("addx ")[1])
            cycle, signal_strength = tick(cycle, register, strengths)
            cycle, signal_strength = tick(cycle, register, strengths)
            register += value

    print(f"Part 1 {sum(signal_strength)}")

    cycle = 1
    register = 1
    grid = [["." for i in range(40)] for i in range(6)]
    for line in input:
        if line == "noop":
            cycle, grid = tick2(cycle, register, grid)
        elif line.startswith("addx"):
            value = int(line.split("addx ")[1])
            cycle, grid = tick2(cycle, register, grid)
            cycle, grid = tick2(cycle, register, grid)
            register += value

    print("Part 2")
    print_grid(grid)


if __name__ == "__main__":
    main(get_input(10, example=False, strip=True))
