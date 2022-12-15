import re
from typing import Dict, List, Set, Tuple

from utils import get_input

REGEX = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"

Coord = Tuple[int, int]

Mapping = Dict[Coord, float]
Beacons = Set[Coord]


def manhattan(a: Coord, b: Coord) -> float:
    return abs((a[0] - b[0])) + abs(a[1] - b[1])


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


def main(input: List[str]) -> None:
    mapping, beacons = parse_input(input)
    row_to_check = 2000000
    not_possible = 0
    for x in range(-1_000_000, 5_000_000):
        possible_beacon = (x, row_to_check)
        if possible_beacon in beacons:
            continue
        for prev, current in mapping.items():
            if is_shorter(possible_beacon, prev, current):
                not_possible += 1
                break

    print(f"Part 1 {not_possible}")


if __name__ == "__main__":
    main(get_input(15, False, strip=True))
