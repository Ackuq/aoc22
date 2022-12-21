from functools import cache
from typing import Dict, List, Tuple, cast

from frozendict import frozendict

from utils import get_input

Value = int | Tuple[str, str, str]  # left, operator, right

Mappings = frozendict[str, Value]
ReducedMappings = Dict[str, Value]


def parse_input(input: List[str], part2: bool = False, offset: int = 0) -> Mappings:
    mappings: Dict[str, Value] = {}
    for line in input:
        key, value = line.split(": ")
        if value.isnumeric():
            mappings[key] = int(value)
            if key == "humn":
                mappings[key] += offset  # type: ignore
            continue
        left, operator, right = value.split()
        if part2 and key == "root":
            mappings[key] = (left, "==", right)
            continue
        mappings[key] = (left, operator, right)
    return frozendict(mappings)


@cache
def reduce_value(mappings: Mappings, value: Value) -> int:
    if isinstance(value, int):
        return value
    left_str, operator, right_str = value
    left = reduce_value(mappings, mappings[left_str])
    right = reduce_value(mappings, mappings[right_str])
    return int(eval(f"{left} {operator} {right}"))


def reduce_mappings(mappings: Mappings) -> int:
    reduced_mappings: ReducedMappings = {}
    for key, value in mappings.items():
        reduced_mappings[key] = reduce_value(mappings, value)
    return cast(int, reduced_mappings["root"])


def main(input: List[str]) -> None:
    mappings = parse_input(input)
    reduced = reduce_mappings(mappings)
    print(f"Part 1: {reduced}")
    mappings = parse_input(input, True)
    reduced = reduce_mappings(mappings)
    offset = 0
    while reduced == 0:
        offset += 1
        mappings = parse_input(input, True, -offset)
        reduced = reduce_mappings(mappings)
        if reduced == 1:
            break
        mappings = parse_input(input, True, offset)
        reduced = reduce_mappings(mappings)
    print(f"Part 2: {mappings['humn']}")


if __name__ == "__main__":
    main(get_input(21, False, strip=True))
