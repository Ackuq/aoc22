from typing import List

from utils import get_input


def main(input: List[str]) -> None:
    line = input[0]
    i = 0
    while True:
        sequence = line[i : i + 4]
        if len(set(sequence)) == 4:
            break
        i += 1
    marker_start = i + 4
    print(f"Part 1: {marker_start}")

    i = 0
    while True:
        sequence = line[i : i + 14]
        if len(set(sequence)) == len(sequence):
            break
        i += 1
    marker_start = i + 14
    print(f"Part 2: {marker_start}")


if __name__ == "__main__":
    main(get_input(6, strip=True))
