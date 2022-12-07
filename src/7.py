import sys
from typing import Dict, List, Optional, Tuple

from utils import get_input


class Node:
    def __init__(self, parent: Optional["Node"] = None) -> None:
        self.directories: Dict[str, Node] = {}
        self.files: Dict[str, int] = {}
        self.parent = parent

    def size(self) -> int:
        size = sum(self.files.values())
        for directory in self.directories.values():
            size += directory.size()
        return size

    def part1(self) -> int:
        size = self.size() if self.size() <= 100000 else 0
        for directory in self.directories.values():
            size += directory.part1()
        return size

    def part2(self, to_remove: int, current: int = sys.maxsize) -> int:
        new = current
        for directory in self.directories.values():
            new = directory.part2(to_remove, new)
        my_size = self.size()
        if my_size >= to_remove and my_size < new:
            new = my_size
        return new

    def ls(self, output: List[str]) -> None:
        for line in output:
            left, right = line.split(" ")
            if left.isdigit():
                # Is file
                size = int(left)
                self.files[right] = size
                continue
            self.directories[right] = Node(self)


def parse_command(line: str) -> str:
    return line.removeprefix("$ ")


Parsed = List[Tuple[str, List[str]]]


def parse_input(input: List[str]) -> Parsed:
    parsed: Parsed = []
    current_command = parse_command(input[0])
    output: List[str] = []
    for line in input[1::]:
        if line.startswith("$ "):
            parsed.append((current_command, output))
            current_command = parse_command(line)
            output = []
            continue
        output.append(line)
    parsed.append((current_command, output))
    return parsed


def main(input: List[str]) -> None:
    parsed = parse_input(input)
    root_node = Node()
    current_node = root_node
    for command in parsed:
        if command[0].startswith("cd"):
            destination = command[0].removeprefix("cd ")
            if destination == "..":
                assert current_node.parent is not None
                current_node = current_node.parent
            elif destination == "/":
                current_node = root_node
            else:
                current_node = current_node.directories[destination]
        elif command[0].startswith("ls"):
            current_node.ls(command[1])

    print(f"Part 1: {root_node.part1()}")

    max_space = 40_000_000
    current_space = root_node.size()
    to_remove = current_space - max_space
    print(f"Part 2: {root_node.part2(to_remove)}")


if __name__ == "__main__":
    main(get_input(7, False, strip=True))
