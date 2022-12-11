import math
import re
from typing import Callable, List, cast

from utils import get_input


class Condition:
    def __init__(
        self,
    ) -> None:
        self.mod: int
        self.true: int
        self.false: int

    def __str__(self) -> str:
        return f"x % {self.mod} == 0 ? {self.true} : {self.false}"


class Monkey:
    def __init__(self, id: int) -> None:
        self.id = id
        self.inspected = 0
        self.items: List[int] = []
        self.operation: Callable[[int], int]
        self.condition: Condition = Condition()

    def __str__(self) -> str:
        return f"Monkey {self.id}: {self.items}"


OPERATION_RE = r"Operation: new = (.*)"
ITEMS_RE = r"Starting items: (.*)"
TEST_RE = r"Test: divisible by (.*)"
TRUE_RE = r"If true: throw to monkey (.*)"
FALSE_RE = r"If false: throw to monkey (.*)"


def create_func(operation: str) -> Callable[[int], int]:
    def func(old: int) -> int:
        return cast(int, eval(f"{operation}"))

    return func


def parse_monkeys(input: List[str]) -> List[Monkey]:
    monkeys: List[Monkey] = []
    current_monkey = Monkey(0)
    for line in input:
        if line == "":
            new_id = current_monkey.id + 1
            monkeys.append(current_monkey)
            current_monkey = Monkey(new_id)
            continue
        operation = re.search(OPERATION_RE, line)
        if operation is not None:
            current_monkey.operation = create_func(operation.group(1))
            continue
        items = re.search(ITEMS_RE, line)
        if items is not None:
            items_str = items.group(1)
            current_monkey.items = [int(item) for item in items_str.split(", ")]
            continue
        test = re.search(TEST_RE, line)
        if test is not None:
            current_monkey.condition.mod = int(test.group(1))
            continue
        condition_false = re.search(FALSE_RE, line)
        if condition_false is not None:
            current_monkey.condition.false = int(condition_false.group(1))
            continue
        condition_true = re.search(TRUE_RE, line)
        if condition_true is not None:
            current_monkey.condition.true = int(condition_true.group(1))

    monkeys.append(current_monkey)

    return monkeys


def main(input: List[str]) -> None:
    monkeys = parse_monkeys(input)
    round = 1
    while round <= 20:
        for monkey in monkeys:
            while len(monkey.items) > 0:
                monkey.inspected += 1
                item = monkey.operation(monkey.items.pop(0))
                item = item // 3
                target = (
                    monkey.condition.true
                    if item % monkey.condition.mod == 0
                    else monkey.condition.false
                )
                monkeys[target].items.append(item)
        round += 1
    top2 = sorted([monkey.inspected for monkey in monkeys])[-2::]
    print(f"Part 1: {math.prod(top2)}")
    monkeys = parse_monkeys(input)
    max_prod = math.prod(monkey.condition.mod for monkey in monkeys)
    round = 1
    while round <= 10_000:
        for monkey in monkeys:
            while len(monkey.items) > 0:
                monkey.inspected += 1
                item = monkey.operation(monkey.items.pop(0)) % max_prod
                target = (
                    monkey.condition.true
                    if item % monkey.condition.mod == 0
                    else monkey.condition.false
                )
                monkeys[target].items.append(item)
        round += 1
    top2 = sorted([monkey.inspected for monkey in monkeys])[-2::]
    print(f"Part 1: {math.prod(top2)}")


if __name__ == "__main__":
    main(get_input(11, False, strip=True))
