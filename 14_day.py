import copy
from enum import Enum


with open("14_input.txt") as f:
    raw_data = f.read().strip().splitlines()


class Signature(int, Enum):
    AIR = 0
    ROCK = 1
    MOVING_SAND = 2
    REST_SAND = 3


OFFSET = 400
SIZE = 400
highest_y = 0
scan_data = [[Signature.AIR] * SIZE for _ in range(SIZE)]
for line in raw_data:
    prev_coord = None
    for coord in line.split(" -> "):
        x, y = list(map(int, coord.split(",")))
        if y > highest_y:
            highest_y = y
        x -= OFFSET
        if prev_coord is not None:
            x1, y1 = prev_coord
            if x == x1:
                for y2 in range(min(y, y1), max(y, y1) + 1):
                    scan_data[y2][x] = Signature.ROCK
            elif y == y1:
                for x2 in range(min(x, x1), max(x, x1) + 1):
                    scan_data[y][x2] = Signature.ROCK
        prev_coord = x, y


def sand_fall(scan: list[list[Signature]], x: int, y: int):
    reset_current = scan[y][x] == Signature.MOVING_SAND
    next_x, next_y = None, None
    if (y + 1) > (SIZE - 1) or (x + 1) > (SIZE - 1):
        return False

    if scan[y + 1][x] == Signature.AIR:
        next_x = x
        next_y = y + 1
    elif scan[y + 1][x - 1] == Signature.AIR:
        next_x = x - 1
        next_y = y + 1
    elif scan[y + 1][x + 1] == Signature.AIR:
        next_x = x + 1
        next_y = y + 1

    if next_x is not None and next_y is not None:
        if reset_current:
            scan[y][x] = Signature.AIR
        scan[next_y][next_x] = Signature.MOVING_SAND
        return sand_fall(scan, next_x, next_y)
    else:
        if reset_current:
            scan[y][x] = Signature.REST_SAND
            return True

        return False


def part_1(scan_data):
    data = copy.deepcopy(scan_data)
    i = 0
    while sand_fall(data, 500 - OFFSET, 0):
        i += 1
    return i


def part_2(scan_data):
    data = copy.deepcopy(scan_data)

    for i in range(SIZE):
        data[highest_y + 2][i] = Signature.ROCK
    i = 0
    while sand_fall(data, 500 - OFFSET, 0):
        i += 1

    return i + 1  # include the source of the sand


print("Part 1:", part_1(scan_data))
print("Part 2:", part_2(scan_data))

# 1462 - too low
