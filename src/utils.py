import re
from typing import List, Tuple


def get_input(day: int, example: bool = False, strip: bool = False) -> List[str]:
    name = day if not example else f"{day}_example"
    f = open(f"./inputs/{name}.txt")
    lines = f.readlines()
    if strip:
        lines = [line.strip() for line in lines]
    return lines


Numbers = List[Tuple[List[int], int]]


def get_numbers(input: List[str]) -> Numbers:
    numbers: Numbers = []
    for index, line in enumerate(input):
        digits = re.findall(r"\d+", line)
        if len(digits) > 0:
            numbers.append((digits, index))
    return numbers
