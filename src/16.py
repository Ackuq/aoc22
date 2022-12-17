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
    all_valves = frozenset(mappings.keys())
    # We can consider the valves with rate = 0 to be opened, for simplicity
    already_opened = frozenset(valve for valve, rate in rates.items() if rate == 0)

    @cache
    def find_max_pressure(
        current: str = "AA",
        # We can consider the valves with rate = 0 to be opened, for simplicity
        opened: FrozenSet[Valve] = already_opened,
        time: int = 30,
    ) -> int:

        if time <= 0:
            return 0
        pressures: Set[int] = set()
        if current not in opened and rates[current] != 0:
            pressures.add(
                find_max_pressure(
                    current,
                    opened.union(frozenset([current])),
                    time - 1,
                )
                + rates[current] * (time - 1)
            )
        pressures.update(
            find_max_pressure(tunnel, opened, time - 1) for tunnel in mappings[current]
        )
        best_pressure = max(pressures)
        return best_pressure

    print(f"Part 1: {find_max_pressure()}")

    # Create all possible permutations of who opens the valves
    Permutation = Tuple[FrozenSet[Valve], FrozenSet[Valve]]

    def create_permutations(
        current_valve: Valve, rest: Set[Valve]
    ) -> List[Permutation]:
        # Create scenario where one opens and the other one doesn't
        if len(rest) == 0:
            return [
                (already_opened.union([current_valve]), already_opened),
                (already_opened, already_opened.union([current_valve])),
            ]
        next_value = rest.pop()
        child_permutations = create_permutations(next_value, rest)
        permutations: List[Permutation] = []
        for child_permutation in child_permutations:
            permutations.append(
                (child_permutation[0].union([current_valve]), child_permutation[1])
            )
            permutations.append(
                (child_permutation[0], child_permutation[1].union([current_valve]))
            )
        return permutations

    potential_valves = set(all_valves.difference(already_opened))
    permutations = create_permutations(potential_valves.pop(), potential_valves)
    current_max = 0
    for human_opened, elephant_opened in permutations:
        human = find_max_pressure(opened=human_opened, time=26)
        elephant = find_max_pressure(opened=elephant_opened, time=26)
        combined = human + elephant
        if combined > current_max:
            current_max = combined

    print(f"Part 2: {current_max}")


if __name__ == "__main__":
    main(get_input(16, False, strip=True))
