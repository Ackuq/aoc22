import sys
from typing import List, Set, Tuple, cast

from utils import get_input

sys.setrecursionlimit(6000)

Cube = Tuple[int, int, int]
Boundary = Tuple[range, range, range]
SIDES = set(
    (
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    )
)


def get_exposed(cubes: Set[Cube]) -> int:
    exposed = 0
    for x, y, z in cubes:
        for dx, dy, dz in SIDES:
            if not (x + dx, y + dy, z + dz) in cubes:
                exposed += 1
    return exposed


def fill(
    boundary: Boundary, air: Set[Cube], cubes: Set[Cube], current: Cube
) -> Set[Cube]:
    air.add(current)
    x, y, z = current
    for dx, dy, dz in SIDES:
        new_air = (x + dx, y + dy, z + dz)
        if (
            new_air in air
            or new_air in cubes
            or new_air[0] not in boundary[0]
            or new_air[1] not in boundary[1]
            or new_air[2] not in boundary[2]
        ):
            continue
        air = fill(boundary, air, cubes, new_air)
    return air


def get_air_pockets(cubes: Set[Cube]) -> int:
    air: Set[Cube] = set()
    # Get the boundary
    boundary = cast(Boundary, tuple(range(min(c) - 1, max(c) + 2) for c in zip(*cubes)))
    # Pick arbitrary starting point on the boundary
    start = min(boundary[0]), min(boundary[1]), min(boundary[2])
    # Fill the grid with air
    air = fill(boundary, set(), cubes, start)
    exposed = 0
    for x, y, z in cubes:
        for dx, dy, dz in SIDES:
            coord = (x + dx, y + dy, z + dz)
            if coord in air and coord not in cubes:
                exposed += 1
    return exposed


def main(input: List[str]) -> None:
    cubes: Set[Cube] = set(
        cast(Cube, tuple(map(int, line.split(",")))) for line in input
    )
    print(f"Part 1 {get_exposed(cubes)}")
    print(f"Part 2 {get_air_pockets(cubes)}")


if __name__ == "__main__":
    main(get_input(18, False, strip=True))
