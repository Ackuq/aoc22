from enum import Enum
from typing import List, Tuple

from utils import get_input


class Direction(Enum):
    Up = "U"
    Right = "R"
    Down = "D"
    Left = "L"


Coordinate = Tuple[int, int]


class Snake:
    def __init__(self) -> None:
        self.head: Coordinate = (0, 0)
        self.tail: Coordinate = (0, 0)
        self.tail_history: List[Coordinate] = [(0, 0)]

    def _tail_should_move(self) -> bool:
        # Tail must always be adjacent to head
        return (
            True
            if abs(self.head[0] - self.tail[0]) > 1
            or abs(self.head[1] - self.tail[1]) > 1
            else False
        )

    def move(self, direction: Direction) -> None:
        old_head = self.head
        if direction is Direction.Up:
            self.head = (self.head[0], self.head[1] + 1)
        elif direction is Direction.Down:
            self.head = (self.head[0], self.head[1] - 1)
        elif direction is Direction.Right:
            self.head = (self.head[0] + 1, self.head[1])
        elif direction is Direction.Left:
            self.head = (self.head[0] - 1, self.head[1])

        if self._tail_should_move():
            self.tail = old_head
            if self.tail not in self.tail_history:
                self.tail_history.append(self.tail)


class Tail:
    def __init__(self, length: int) -> None:
        self.id = length
        self.coordinates: Coordinate = (0, 0)
        self.tail = Tail(length - 1) if length > 1 else None
        self.tail_history: List[Coordinate] = [(0, 0)]

    def _should_move(self, new_head: Coordinate) -> bool:
        # Tail must always be adjacent to head
        return (
            True
            if abs(new_head[0] - self.coordinates[0]) > 1
            or abs(new_head[1] - self.coordinates[1]) > 1
            else False
        )

    def move(self, new_parent: Coordinate) -> None:
        # Tail must always be adjacent to head
        if not self._should_move(new_parent):
            return

        y_direction = 0
        x_direction = 0
        if new_parent[0] > self.coordinates[0]:
            # Move right
            x_direction += 1
        elif new_parent[0] < self.coordinates[0]:
            # Move left
            x_direction -= 1
        if new_parent[1] > self.coordinates[1]:
            # Move up
            y_direction += 1
        elif new_parent[1] < self.coordinates[1]:
            # Move down
            y_direction -= 1
        self.coordinates = (
            self.coordinates[0] + x_direction,
            self.coordinates[1] + y_direction,
        )
        if self.coordinates not in self.tail_history:
            self.tail_history.append(self.coordinates)
        if self.tail is not None:
            self.tail.move(self.coordinates)


class Head:
    def __init__(self, length: int) -> None:
        self.coordinates: Coordinate = (0, 0)
        self.tail = Tail(length)

    def move(self, direction: Direction) -> None:
        if direction is Direction.Up:
            self.coordinates = (self.coordinates[0], self.coordinates[1] + 1)
        elif direction is Direction.Down:
            self.coordinates = (self.coordinates[0], self.coordinates[1] - 1)
        elif direction is Direction.Right:
            self.coordinates = (self.coordinates[0] + 1, self.coordinates[1])
        elif direction is Direction.Left:
            self.coordinates = (self.coordinates[0] - 1, self.coordinates[1])

        self.tail.move(self.coordinates)


Command = Tuple[Direction, int]


def parse_input(input: List[str]) -> List[Command]:
    result: List[Command] = []
    for line in input:
        direction, times = line.split(" ")
        result.append((Direction(direction), int(times)))
    return result


def main(input: List[str]) -> None:
    commands = parse_input(input)
    snake = Snake()
    for direction, times in commands:
        for _ in range(times):
            snake.move(direction)
    print(f"Part 1 {len(snake.tail_history)}")

    head = Head(9)
    for direction, times in commands:
        for _ in range(times):
            head.move(direction)
    current_tail = head.tail
    while current_tail.tail is not None:
        current_tail = current_tail.tail
    print(f"Part 2 {len(current_tail.tail_history)}")


if __name__ == "__main__":
    main(get_input(9, False, strip=True))
