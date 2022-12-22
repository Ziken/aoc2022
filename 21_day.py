def traverse_monkeys(monkeys, current_m):
    value = monkeys[current_m]
    try:
        if value.isnumeric():
            return int(value)
    except AttributeError:  # is complex number :)
        return value

    first_monkey, operation, second_monkey = value.split(" ")
    val_1 = traverse_monkeys(monkeys, first_monkey)
    val_2 = traverse_monkeys(monkeys, second_monkey)
    v = 0
    match operation:
        case "+":
            v = val_1 + val_2
        case "-":
            v = val_1 - val_2
        case "*":
            v = val_1 * val_2
        case "/":
            v = val_1 / val_2

    monkeys[current_m] = v
    return v


def part_1(monkeys):
    c = monkeys.copy()
    return int(traverse_monkeys(c, "root"))


def part_2(monkeys):
    c = monkeys.copy()
    c["humn"] = 1j
    root = monkeys["root"]
    left_monkey, _, right_monkey = root.split(" ")
    left_value = traverse_monkeys(c, left_monkey)
    right_value = traverse_monkeys(c, right_monkey)
    if isinstance(right_value, complex):
        left_value, right_value = right_value, left_value

    right_value -= left_value.real
    return round(right_value / left_value.imag)


with open("21_input.txt") as f:
    raw_input = f.read().strip().splitlines()

monkeys = {m: o for m, o in map(lambda x: x.split(": "), raw_input)}
print("Part 1:", part_1(monkeys))
print("Part 2:", part_2(monkeys))
