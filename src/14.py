import itertools
from typing import Iterable, List, Set, Tuple

from utils import get_input

Coord = Tuple[int, int]


def pairwise(coords: List[Coord]) -> Iterable[Tuple[Coord, Coord]]:
    a, b = itertools.tee(coords)
    next(b, None)
    return zip(a, b)


def parse_input(input: List[str]) -> Set[Coord]:
    blocked: Set[Coord] = set()
    for line in input:
        coords_str = line.split(" -> ")
        coords: List[Coord] = [
            (int(coord[0]), int(coord[1]))
            for coord in [coord_str.split(",") for coord_str in coords_str]
        ]
        for coord_from, coord_to in pairwise(coords):
            x_0, y_0 = coord_from
            x_1, y_1 = coord_to
            x_range = range(min(x_1, x_0), max(x_1, x_0) + 1)
            y_range = range(min(y_1, y_0), max(y_1, y_0) + 1)
            for y in y_range:
                for x in x_range:
                    blocked.add((x, y))
    return blocked


def main(input: List[str]) -> None:
    blocked = parse_input(input)
    sand_pos = (500, 0)
    round = 0
    current_sand = sand_pos
    not_found_counter = 0
    while True:
        down = (current_sand[0], current_sand[1] + 1)
        hori_left = (current_sand[0] - 1, current_sand[1] + 1)
        hori_right = (current_sand[0] + 1, current_sand[1] + 1)
        if down not in blocked:
            current_sand = down
            not_found_counter += 1
            if not_found_counter > 100:
                break
            continue
        if hori_left not in blocked:
            current_sand = hori_left
            continue
        if hori_right not in blocked:
            current_sand = hori_right
            continue
        not_found_counter = 0
        round += 1
        blocked.add(current_sand)
        current_sand = sand_pos

    print(f"Part 1 {round}")

    blocked = parse_input(input)
    sand_pos = (500, 0)
    highest_y = max(coord[1] for coord in blocked) + 2
    round = 0
    current_sand = sand_pos
    while sand_pos not in blocked:
        down = (current_sand[0], current_sand[1] + 1)
        hori_left = (current_sand[0] - 1, current_sand[1] + 1)
        hori_right = (current_sand[0] + 1, current_sand[1] + 1)
        is_highest_y = current_sand[1] + 1 == highest_y
        if not is_highest_y:
            if down not in blocked:
                current_sand = down
                continue
            if hori_left not in blocked:
                current_sand = hori_left
                continue
            if hori_right not in blocked:
                current_sand = hori_right
                continue
        round += 1
        blocked.add(current_sand)
        current_sand = sand_pos

    print(f"part 2 {round}")


if __name__ == "__main__":
    main(get_input(14, False, strip=True))
