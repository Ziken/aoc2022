import functools


with open("13_input.txt") as f:
    data = f.read().strip().splitlines()


def find_valid_packets(first, second):
    for left, right in zip(first, second):
        if isinstance(left, list) and isinstance(right, list):
            a = find_valid_packets(left, right)
            if a is not None:
                return a
        elif isinstance(left, int) and isinstance(right, list):
            a = find_valid_packets([left], right)
            if a is not None:
                return a

        elif isinstance(left, list) and isinstance(right, int):
            a = find_valid_packets(left, [right])
            if a is not None:
                return a
        elif left == right:
            continue
        elif left < right:
            return True
        else:
            return False

    if len(first) < len(second):
        return True
    if len(first) > len(second):
        return False

    return None


def order_packets(first, second):
    for left, right in zip(first, second):
        if isinstance(left, list) and isinstance(right, list):
            a = order_packets(left, right)
            if a != 0:
                return a
        elif isinstance(left, int) and isinstance(right, list):
            a = order_packets([left], right)
            if a != 0:
                return a
        elif isinstance(left, list) and isinstance(right, int):
            a = order_packets(left, [right])
            if a != 0:
                return a
        elif left == right:
            continue
        elif left < right:
            return -1
        else:
            return 1

    if len(first) < len(second):
        return -1
    if len(first) > len(second):
        return 1

    return 0


def part_1():
    s = 0
    for no_pair, i in enumerate(range(0, len(data), 3)):
        a = find_valid_packets(eval(data[i]), eval(data[i + 1]))
        if a > 0:
            s += no_pair + 1

    return s


def part_2():
    packets = [eval(d) for d in data if d]
    packets.extend([[[2]], [[6]]])
    packets.sort(key=functools.cmp_to_key(order_packets))

    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


print("Part 1:", part_1())
print("Part 2:", part_2())
