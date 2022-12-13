import ast
import math
from functools import cmp_to_key
from typing import List, Tuple

from more_itertools import flatten

from utils import get_input

Node = int | List["Node"]
Pair = Tuple[Node, Node]


def parse_input(input: List[str]) -> List[Pair]:
    string_pairs = list(zip(*[iter([line for line in input if line != ""])] * 2))
    pairs: List[Pair] = []
    for left_str, right_str in string_pairs:
        left = ast.literal_eval(left_str)
        right = ast.literal_eval(right_str)
        pairs.append((left, right))
    return pairs


def compare(left: "Node", right: "Node") -> int:
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    if isinstance(left, list) and isinstance(right, list):
        for le, re in zip(left, right):
            cmp = compare(le, re)
            if cmp != 0:
                return cmp
        return compare(len(left), len(right))
    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    return True


def main(input: List[str]) -> None:
    pairs = parse_input(input)
    indicies: List[int] = []
    for i, (left, right) in enumerate(pairs):
        if compare(left, right) < 0:
            indicies.append(i + 1)
    print(f"Part 1 {sum(indicies)}")

    dividers: List[Node] = [[[2]], [[6]]]
    all_nodes = list(flatten(pairs)) + dividers
    sorted_nodes = sorted(all_nodes, key=cmp_to_key(compare))
    prod = math.prod(
        i for i, value in enumerate(sorted_nodes, start=1) if value in dividers
    )
    print(f"Part 2: {prod}")


if __name__ == "__main__":
    main(get_input(13, False, strip=True))
