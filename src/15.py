import re
from typing import Dict, List, Set, Tuple

from utils import get_input

REGEX = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"

Coord = Tuple[int, int]

Mapping = Dict[Coord, int]
Beacons = Set[Coord]


def manhattan(a: Coord, b: Coord) -> int:
    return int(abs((a[0] - b[0])) + abs(a[1] - b[1]))


def parse_input(input: List[str]) -> Tuple[Mapping, Beacons]:
    mapping: Mapping = {}
    beacons: Beacons = set()
    for line in input:
        match = re.search(REGEX, line)
        assert match is not None
        coord = [int(x) for x in match.groups()]
        sensor = (coord[0], coord[1])
        beacon = (coord[2], coord[3])
        beacons.add(beacon)
        mapping[sensor] = manhattan(sensor, beacon)
    return mapping, beacons


def is_shorter(possible: Coord, sensor: Coord, old_dist: float) -> bool:
    new_dist = manhattan(sensor, possible)
    return new_dist <= old_dist


def add_invalid(y: int, mapping: Mapping, beacons: Beacons) -> Set[Coord]:
    invalid: Set[Coord] = set()
    for sensor, dist in mapping.items():
        radius_y = int(abs(sensor[1] - y))
        max_radius_x = dist - radius_y
        if max_radius_x >= 0:
            for dx in range(-max_radius_x, max_radius_x + 1):
                dest = (sensor[0] + dx, y)
                if dest not in beacons:
                    invalid.add(dest)
    return invalid


def add_invalid2(
    y: int, mapping: Mapping, beacons: Beacons, maximum: int
) -> Set[Coord]:
    invalid: Set[Coord] = set()
    for sensor, dist in mapping.items():
        if len(invalid) == maximum - 1:
            break
        radius_y = int(abs(sensor[1] - y))
        max_radius_x = dist - radius_y
        if max_radius_x >= 0:
            minimum = max(0, sensor[0] - max_radius_x)
            maximum_i = min(maximum, max_radius_x + sensor[0])
            invalid.add((minimum, maximum_i))
    return invalid


def main(input: List[str]) -> None:
    mapping, beacons = parse_input(input)
    # row_to_check = 10
    row_to_check = 2000000
    invalid: Set[Coord] = add_invalid(row_to_check, mapping, beacons)

    # print(f"Part 1 {len(invalid)}")

    maximum = 4000000
    # maximum = 20
    multiply = 4000000
    found = False
    last_x = 0
    for y in range(maximum + 1):
        invalid = add_invalid2(y, mapping, beacons, maximum)
        last_x = 0
        for x_range in sorted(invalid):
            min_x, max_x = x_range
            if last_x < min_x:
                found = True
                break
            if max_x >= last_x:
                last_x = max_x + 1
        if found:
            break

    print(f"Part 2 {last_x * multiply + y}")


if __name__ == "__main__":
    main(get_input(15, False, strip=True))
