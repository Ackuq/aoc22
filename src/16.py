import re
from typing import Dict, List, Tuple

from utils import get_input

Valve = str

Mappings = Dict[Valve, List[Valve]]
Rates = Dict[Valve, int]

INPUT_RE = "Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)"


def parse_input(input: List[str]) -> Tuple[Mappings, Rates]:
    mappings: Mappings = {}
    rates: Rates = {}
    for line in input:
        match = re.search(INPUT_RE, line)
        assert match is not None
        valve, rate_str, to_str = match.groups()
        to = [v for v in to_str.split(", ")]
        rate = int(rate_str)
        mappings[valve] = to
        rates[valve] = rate

    return mappings, rates


def main(input: List[str]) -> None:
    mappings, rates = parse_input(input)
    print(mappings)
    print(rates)


if __name__ == "__main__":
    main(get_input(16, True, strip=True))
