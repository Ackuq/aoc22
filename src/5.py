import re
from typing import List, Tuple

from utils import get_input


class Stack:
    def __init__(self) -> None:
        self.stack: List[str] = []

    def pop(self) -> str:
        return self.stack.pop(0)

    def push(self, char: str) -> None:
        self.stack.insert(0, char)

    def take_n(self, n: int) -> List[str]:
        sub_stack = self.stack[:n]
        self.stack = self.stack[n::]
        return sub_stack

    def add_n(self, sub_stack: List[str]) -> None:
        self.stack = sub_stack + self.stack

    def __str__(self) -> str:
        return self.stack.__str__()


Move = Tuple[int, int, int]

bucket_line = r"^(?:\s+\d+)+$"
buckets_capture = r"(?:\s+(\d+))"


def print_stacks(stacks: List[Stack]) -> None:
    for i, stack in enumerate(stacks):
        print(f"{i +1}: {stack}")


def parse_input(input: List[str]) -> Tuple[List[Stack], List[Move]]:
    stacks: List[Stack] = []
    move_line: int = 0

    for index_line, line in enumerate(input):
        if re.match(bucket_line, line) is not None:
            for index_char, char in enumerate(line):
                if char.isdigit():
                    stack = Stack()
                    index_stack = index_line - 1
                    current_char = input[index_stack][index_char]
                    while current_char.isalpha():
                        stack.push(current_char)
                        index_stack = index_stack - 1
                        if (index_stack) < 0 or len(
                            input[index_stack]
                        ) < index_char + 1:
                            break
                        current_char = input[index_stack][index_char]
                    stacks.append(stack)
            move_line = index_line + 2
            break
    move_instructions = input[move_line::]
    moves: List[Move] = []
    for instruction in move_instructions:
        groups = re.findall(r"\d+", instruction)
        moves.append(tuple([int(s) for s in groups]))  # type: ignore

    return stacks, moves


def main(input: List[str]) -> None:
    stacks, moves = parse_input(input)
    for move in moves:
        amount = move[0]
        origin = move[1] - 1
        destination = move[2] - 1
        for _ in range(amount):
            if len(stacks[origin].stack) < 1:
                break
            stacks[destination].push(stacks[origin].pop())
    part1 = ""
    for stack in stacks:
        part1 += stack.stack[0]
    print(f"Part 1: {part1}")

    stacks, moves = parse_input(input)
    for move in moves:
        origin = move[1] - 1
        destination = move[2] - 1
        amount = min(move[0], len(stacks[origin].stack))
        stacks[destination].add_n(stacks[origin].take_n(amount))
    part2 = ""
    for stack in stacks:
        part2 += stack.stack[0]
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main(get_input(5, True))
