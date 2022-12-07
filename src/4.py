from typing import List, Tuple

from utils import get_input


def main(input: List[str]) -> None:
    range_pairs: List[Tuple[range, range]] = []
    for line in input:
        elf1_str, elf2_str = line.split(",")
        elf1_num = elf1_str.split("-")
        elf2_num = elf2_str.split("-")
        range_pairs.append(
            (
                range(int(elf1_num[0]), int(elf1_num[1]) + 1),
                range(int(elf2_num[0]), int(elf2_num[1]) + 1),
            )
        )
    overlaps = 0
    for elf1, elf2 in range_pairs:
        if (elf1.start in elf2 and elf1[-1] in elf2) or (
            elf2.start in elf1 and elf2[-1] in elf1
        ):
            overlaps += 1
    print(f"Part 1: {overlaps}")

    overlaps = 0
    for elf1, elf2 in range_pairs:
        for num in elf1:
            if num in elf2:
                overlaps += 1
            else:
                continue
            break
    print(f"Part 2: {overlaps}")


if __name__ == "__main__":
    main(get_input(4, strip=True))
