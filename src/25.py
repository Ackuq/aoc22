from typing import List

from utils import get_input

mapping = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}
inv_mapping = {v: k for k, v in mapping.items()}


def parse_snafu(snafu: str) -> int:
    result = 0
    for i, char in enumerate(reversed(snafu)):
        decimal = mapping[char]
        result += decimal * (5**i)
    return result


def parse_decimal(decimal: int) -> str:
    snafu = ""
    rest = decimal
    while rest > 0:
        remainder = ((rest + 2) % 5) - 2
        snafu = inv_mapping[remainder] + snafu
        rest = (rest + 2) // 5
    return snafu


def main(input: List[str]) -> None:
    decimal = sum(parse_snafu(line) for line in input)
    print(f"Part 1: {parse_decimal(decimal)}")


if __name__ == "__main__":
    main(get_input(25, False, strip=True))
