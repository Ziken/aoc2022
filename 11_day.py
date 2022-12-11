import copy
import dataclasses
from dataclasses import dataclass
from typing import Callable, Optional

# @dataclass(frozen=True)
@dataclass
class Operation:
    operation: str
    value: int

    def perform(self, i: int, mod: int) -> int:
        if self.operation == "+":
            return i + (self.value % mod)
        elif self.operation == "*":
            return i * (self.value % mod)
        elif self.operation == "**":
            return i * i


@dataclass
class Item:
    worry_level: int
    operations_history: list[Operation] = dataclasses.field(default_factory=list)

    def inspect(self):
        self.worry_level //= 3

    def optimize(self):
        new_history = [self.operations_history[0]]
        for o in self.operations_history[1:]:
            if new_history[-1].operation == o.operation:
                if o.operation == "+":
                    new_history[-1].value += o.value
                elif o.operation == "*":
                    new_history[-1].value *= o.value
            else:
                new_history.append(o)

        self.operations_history = new_history

    def get_value(self, mod: int) -> int:
        if len(self.operations_history) % 1000 == 0:
            self.optimize()

        current_level = self.worry_level
        for o in self.operations_history:
            current_level = o.perform(current_level, mod)
            current_level %= mod

        return current_level


@dataclass
class Monkey:
    id: int
    items: list[Item]
    throw_to: list[int]
    n: int = 0
    condition: int = 0
    operation: str = None
    inspect_count: int = 0

    def add_item(self, item: Item):
        self.items.append(item)

    def perform_operation(self, item: Item):
        if self.operation == "+":
            item.worry_level += self.n
        elif self.operation == "*":
            item.worry_level *= self.n
        elif self.operation == "**":
            item.worry_level *= item.worry_level

    def perform_operation_ridiculous(self, item: Item):
        if self.operation == "+":
            item.operations_history.append(Operation("+", self.n))
        elif self.operation == "*":
            item.operations_history.append(Operation("*", self.n))
        elif self.operation == "**":
            item.operations_history.append(Operation("**", -1))

    def throw(self):
        for item in self.items:
            self.inspect_count += 1
            self.perform_operation(item)
            item.inspect()
            yield item, self.throw_to[(item.worry_level % self.condition) != 0]

        self.items = []

    def throw_ridiculous(self):
        for item in self.items:
            self.inspect_count += 1
            self.perform_operation_ridiculous(item)
            current_level = item.get_value(self.condition)
            yield item, self.throw_to[current_level != 0]

        self.items = []


def parse_data(data):
    monkeys = dict()
    # parse raw_dat
    monkey_id = 1
    for line in data:
        if line.startswith("Monkey"):
            monkey_id = int(line.split()[1][:-1])
            monkeys[monkey_id] = Monkey(monkey_id, [], [])
        elif line.startswith("  Starting items"):
            items = line.split(":")[1].strip().split(",")
            for item in items:
                monkeys[monkey_id].items.append(Item(int(item)))
        elif line.startswith("  Operation"):
            operation = line.split(":")[1].strip()
            if operation.startswith("new = old * old"):
                monkeys[monkey_id].operation = "**"
                monkeys[monkey_id].n = ""
            elif operation.startswith("new = old *"):
                monkeys[monkey_id].operation = "*"
                n = int(operation.split("*")[1])
                monkeys[monkey_id].n = n
            elif operation.startswith("new = old +"):
                n = int(operation.split("+")[1])
                monkeys[monkey_id].operation = "+"
                monkeys[monkey_id].n = n

        elif line.startswith("  Test"):
            test = line.split(":")[1].strip()
            if test.startswith("divisible by"):
                monkeys[monkey_id].condition = int(test.split(" ")[2])

        elif line.startswith("    If true"):
            monkeys[monkey_id].throw_to.append(int(line.split()[-1]))
        elif line.startswith("    If false"):
            monkeys[monkey_id].throw_to.append(int(line.split()[-1]))

    return monkeys


def part_1(monkeys) -> int:
    for r in range(20):
        for monkey in monkeys.values():
            # for item, throw_to in monkey.throw_test():
            for item, throw_to in monkey.throw():
                monkeys[throw_to].add_item(item)

    a = sorted(map(lambda x: x.inspect_count, monkeys.values()), reverse=True)
    return a[0] * a[1]


def part_2(monkeys):
    for r in range(10_000):
        for monkey in monkeys.values():
            # for item, throw_to in monkey.throw_test():
            for item, throw_to in monkey.throw_ridiculous():
                monkeys[throw_to].add_item(item)

    a = sorted(map(lambda x: x.inspect_count, monkeys.values()), reverse=True)
    return a[0] * a[1]


with open("11_input.txt") as f:
    raw_data = f.read().splitlines()

monkeys_part_1 = parse_data(raw_data)
monkeys_part_2 = copy.deepcopy(monkeys_part_1)

print("part 1:", part_1(monkeys_part_1))
print("part 2:", part_2(monkeys_part_2))
