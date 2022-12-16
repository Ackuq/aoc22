import re
from functools import cache
from typing import Dict, FrozenSet, List, Set, Tuple

from utils import get_input

Valve = str

Mappings = Dict[Valve, Set[Valve]]
Rates = Dict[Valve, int]

INPUT_RE = "Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)"


def parse_input(input: List[str]) -> Tuple[Mappings, Rates]:
    mappings: Mappings = {}
    rates: Rates = {}
    for line in input:
        match = re.search(INPUT_RE, line)
        assert match is not None
        valve, rate_str, to_str = match.groups()
        to = set([v for v in to_str.split(", ")])
        rate = int(rate_str)
        mappings[valve] = to
        rates[valve] = rate

    return mappings, rates


def main(input: List[str]) -> None:
    mappings, rates = parse_input(input)

    @cache
    def find_max_pressure(
        current: str,
        opened: FrozenSet[Valve] = frozenset(),
        time: int = 30,
    ) -> int:
        if time <= 0:
            return 0
        pressures: Set[int] = set()
        if current not in opened:
            pressures.add(
                find_max_pressure(
                    current,
                    opened.union(frozenset([current])),
                    time - 1,
                )
                + rates[current] * (time - 1)
            )
        pressures = pressures.union(
            find_max_pressure(tunnel, opened, time - 1) for tunnel in mappings[current]
        )
        best_pressure = max(pressures)
        return best_pressure

    print(f"Part 1: {find_max_pressure('AA')}")


if __name__ == "__main__":
    main(get_input(16, False, strip=True))
