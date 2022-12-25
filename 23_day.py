import math
from collections import defaultdict
from enum import Enum

with open("23_input.txt") as f:
    raw_input = f.read().strip().splitlines()


class Direction(int, Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3

def check_north(elves, position):
    # Check N, NE, NW
    for x, y in [(0, -1), (1, -1), (-1, -1)]:
        if (position[0] + x, position[1] + y) in elves:
            return None

    return (position[0], position[1] - 1)


def check_south(elves, position):
    # Check S, SE, SW
    for x, y in [(0, 1), (1, 1), (-1, 1)]:
        if (position[0] + x, position[1] + y) in elves:
            return None

    return (position[0], position[1] + 1)


def check_west(elves, position):
    # Check W, NW, SW
    for x, y in [(-1, 0), (-1, -1), (-1, 1)]:
        if (position[0] + x, position[1] + y) in elves:
            return None

    return (position[0] - 1, position[1])


def check_east(elves, position):
    # Check E, NE, SE
    for x, y in [(1, 0), (1, -1), (1, 1)]:
        if (position[0] + x, position[1] + y) in elves:
            return None

    return (position[0] + 1, position[1])

DIRECTION_MAP = {
    Direction.NORTH: check_north,
    Direction.SOUTH: check_south,
    Direction.WEST: check_west,
    Direction.EAST: check_east,
}

def get_proposed_position(elves, position, direction: Direction):
    # check all 8 directions
    for x, y in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
        new_pos = (position[0] + x, position[1] + y)
        if new_pos in elves:
            break
    else:
        return None

    for i in range(4):
        new_pos = DIRECTION_MAP[(direction+i) % 4](elves, position)
        if new_pos:
            return new_pos

    return None


def perform_round(old_positions, direction: Direction):
    proposed_positions = defaultdict(list)
    for elf in old_positions:
        proposed_pos = get_proposed_position(old_positions, elf, direction)
        if proposed_pos:
            proposed_positions[proposed_pos].append(elf)

    for proposed_position, elves in proposed_positions.items():
        if len(elves) > 1:
            continue

        old_position = elves[0]
        new_position = proposed_position
        old_positions.remove(old_position)
        old_positions.add(new_position)

def get_area(elves):
    up_left_pos = (math.inf, -math.inf)
    down_right_pos = (-math.inf, math.inf)

    for x, y in elves:
        up_left_pos = (min(up_left_pos[0], x), max(up_left_pos[1], y))
        down_right_pos = (max(down_right_pos[0], x), min(down_right_pos[1], y))
    # Get square area
    return (down_right_pos[0] - up_left_pos[0] + 1) * (up_left_pos[1] - down_right_pos[1] + 1) - len(elves)

def part_1(elves):
    elves_positions = elves.copy()
    priority_direction = Direction.NORTH
    for _ in range(10):
        perform_round(elves_positions, priority_direction)
        priority_direction = (priority_direction + 1) % 4

    return get_area(elves_positions)

def part_2(elves):
    elves_positions = elves.copy()
    old_positions = set()
    priority_direction = Direction.NORTH
    elf_round = 0
    while elves_positions != old_positions:
        old_positions = elves_positions.copy()
        perform_round(elves_positions, priority_direction)
        priority_direction = (priority_direction + 1) % 4
        elf_round += 1

    return elf_round

elves_positions = set()
for y, line in enumerate(raw_input):
    for x, sign in enumerate(line):
        if sign == "#":
            elves_positions.add((x, y))

print("Part 1:", part_1(elves_positions))
print("Part 2:", part_2(elves_positions))

