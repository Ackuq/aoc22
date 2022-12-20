from typing import List, Tuple

from tqdm import tqdm

from utils import get_input

File = List[int]


def print_file(file: List[Tuple[int, int]]) -> None:
    print(", ".join(str(x[0]) for x in file))


class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.backward: "Node"
        self.forward: "Node"

    def set_backward(self, node: "Node") -> None:
        self.backward = node

    def set_forward(self, node: "Node") -> None:
        self.forward = node

    def move(self, direction: int) -> None:
        while direction < 0:
            old_backward_backward = self.backward.backward
            # Make the one in between us reference each other
            self.forward.backward = self.backward
            self.backward.forward = self.forward
            # Put us behind the previous one
            self.backward.backward = self
            self.forward = self.backward
            # We become the one ahead of the one behind the previous one
            self.backward = old_backward_backward
            old_backward_backward.forward = self
            direction += 1
        while direction > 0:
            old_forward_forward = self.forward.forward
            # Make the one in between us reference each other
            self.forward.backward = self.backward
            self.backward.forward = self.forward
            # Put us ahead of the next one
            self.forward.forward = self
            self.backward = self.forward
            # We become the one before of the one ahead the previous one
            self.forward = old_forward_forward
            old_forward_forward.backward = self
            direction -= 1

    def __repr__(self) -> str:
        return f"{self.backward.value} <- {self.value} -> {self.forward.value}"


def mixing(numbers: List[int], times: int) -> List[Node]:
    nodes = [Node(num) for num in numbers]
    # Connect the nodes
    for i, node in enumerate(nodes):
        node.set_forward(nodes[(i + 1) % len(nodes)])
        node.set_backward(nodes[i - 1])
    progress = tqdm(total=times * len(nodes))
    for _ in range(times):
        for node in nodes:
            direction = (
                node.value % (len(nodes) - 1)
                if node.value > 0
                else node.value % (-len(nodes) + 1)
            )
            node.move(direction)
            progress.update(1)
    return nodes


def get_result(nodes: List[Node]) -> int:
    result = 0
    current_node = next(node for node in nodes if node.value == 0)
    for i in range(0, 3001):
        if i % 1000 == 0 and i != 0:
            result += current_node.value
        current_node = current_node.forward
    return result


def main(input: List[str]) -> None:
    numbers = [int(num) for num in input]
    nodes = mixing(numbers, 1)
    print(f"Part 1: {get_result(nodes)}")
    # Reset the nodes
    numbers = [int(num) * 811589153 for num in input]
    nodes = mixing(numbers, 10)
    print(f"Part 2: {get_result(nodes)}")


if __name__ == "__main__":
    main(get_input(20, False, strip=True))
