from typing import Generator, List, Set, Tuple

from tqdm import tqdm

from utils import get_input

MAX_X = 6

Coord = Tuple[int, int]
Rock = Set[Coord]

ROCK_1: Rock = set([(2, 0), (3, 0), (4, 0), (5, 0)])
ROCK_2: Rock = set([(2, 1), (3, 2), (3, 1), (3, 0), (4, 1)])
ROCK_3: Rock = set([(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)])
ROCK_4: Rock = set([(2, 0), (2, 1), (2, 2), (2, 3)])
ROCK_5: Rock = set([(2, 0), (2, 1), (3, 0), (3, 1)])

ROCKS = [ROCK_1, ROCK_2, ROCK_3, ROCK_4, ROCK_5]


def get_rock_generator() -> Generator[Rock, None, None]:
    while True:
        for rock in ROCKS:
            yield rock


def get_move_generator(line: str) -> Generator[str, None, None]:
    while True:
        for char in line:
            yield char


def is_done(current_rock: Rock, occupied: Set[Coord]) -> bool:
    # Check if any y coord is 0
    for x, y in current_rock:
        if y == 0 or (x, y - 1) in occupied:
            return True
    return False


def print_rock(current_rock: Rock, occupied: Set[Coord], max_y: int) -> None:
    top = max(max_y, *(y for _, y in current_rock)) + 1
    grid = [["." for _ in range(7)] for _ in range(top)]
    for y in range(top):
        for x in range(7):
            coord = (x, y)
            if coord in current_rock:
                grid[y][x] = "@"
            elif coord in occupied:
                grid[y][x] = "#"
            else:
                grid[y][x] = "."
    grid.reverse()
    print("\n".join(["".join(line) for line in grid]))


def do_move(current_rock: Rock, current_move: str, occupied: Set[Coord]) -> Rock:
    new_rock: Rock = set()
    delta = 1 if current_move == ">" else -1
    for x, y in current_rock:
        if current_move == ">" and x == MAX_X:
            return current_rock
        if current_move == "<" and x == 0:
            return current_rock
        new_coord = (x + delta, y)
        if new_coord in occupied:
            return current_rock
        new_rock.add(new_coord)
    return new_rock


def run(max_rocks: int, moves: str) -> int:
    occupied: Set[Coord] = set()
    fallen_rocks = 0
    rock_generator = get_rock_generator()
    move_generator = get_move_generator(moves)
    max_y = 0
    progress_bar = tqdm(total=max_rocks)
    while fallen_rocks < max_rocks:
        current_rock = next(rock_generator)
        current_rock = set([(x, y + max_y + 3) for x, y in current_rock])

        current_move = next(move_generator)
        current_rock = do_move(current_rock, current_move, occupied)
        while not is_done(current_rock, occupied):
            current_rock = set([(x, y - 1) for x, y in current_rock])
            current_move = next(move_generator)
            current_rock = do_move(current_rock, current_move, occupied)

        max_y = max(max_y, *(y + 1 for _, y in current_rock))
        occupied.update(current_rock)
        fallen_rocks += 1
        progress_bar.update(1)
    return max_y


def main(input: List[str]) -> None:
    part1 = run(2022, input[0])
    print(f"Part 1: {part1}")
    part2 = run(1_000_000_000, input[0])
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main(get_input(17, True, strip=True))
