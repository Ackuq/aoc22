from typing import List

from utils import get_input


def main(input: List[str]) -> None:
    elves: List[int] = []
    current_elf = 0

    for line in input:
        stripped = line.strip()
        if stripped == "":
            elves.append(current_elf)
            current_elf = 0
            continue
        calories = int(stripped)
        current_elf += calories
    elves.append(current_elf)
    print(f"Part 1: {max(elves)}")

    sorted_elves = sorted(elves)
    top_3 = sorted_elves[-3::]
    print(f"Part 2: {sum(top_3)}")


if __name__ == "__main__":
    main(get_input(1))
