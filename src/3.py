from typing import List, Set

from utils import get_input


def do_sum(chars: Set[str]) -> int:
    sum = 0
    for char in chars:
        value = ord(char) - 96 if char.islower() else ord(char) - 65 + 27
        sum += value
    return sum


def main(input: List[str]) -> None:
    sum = 0
    for line in input:
        middle = len(line) // 2
        compartment1 = set(line[:middle])
        compartment2 = set(line[middle::])
        intersection = compartment1.intersection(compartment2)
        sum += do_sum(intersection)

    print(f"Part 1 {sum}")

    group_index = 0
    sum = 0
    while group_index < len(input) // 3:
        first, *rest = input[group_index * 3 : (group_index * 3) + 3]
        intersection = set(first).intersection(*rest)
        sum += do_sum(intersection)
        group_index += 1

    print(f"Part 2 {sum}")


if __name__ == "__main__":
    main(get_input(3, strip=True))
