import functools
from collections import defaultdict

with open("24_input.txt") as f:
    raw_input = f.read().strip().splitlines()


def mod_num(start, end, num):
    if num == 0:
        num -= start
    num = num % end
    if num == 0:
        return num + start
    return num


def perform_move(
    blizzard_map: dict[tuple[int, int], list[str]], border_x: int, border_y: int
):
    mod_x = functools.partial(mod_num, 1, border_x - 1)
    mod_y = functools.partial(mod_num, 1, border_y - 1)
    new_map = defaultdict(list)
    for (x, y), blizzards in blizzard_map.items():
        for blizzard in blizzards:
            if blizzard == ">":
                new_map[(mod_x(x + 1), y)].append(">")
            elif blizzard == "<":
                new_map[(mod_x(x - 1), y)].append("<")
            elif blizzard == "^":
                new_map[(x, mod_y(y - 1))].append("^")
            elif blizzard == "v":
                new_map[(x, mod_y(y + 1))].append("v")
            elif blizzard == "#":
                new_map[(x, y)].append("#")

    return new_map


def go_through_blizzard(
    blizzard_map,
    start_point: tuple[int, int],
    end_point: tuple[int, int],
    size_x: int,
    size_y: int,
):
    current_positions = {start_point}
    minutes = 0
    current_map = blizzard_map
    while True:
        if end_point in current_positions:
            return current_map, minutes - 1

        minutes += 1
        next_positions = set()
        for x, y in current_positions:
            for new_x, new_y in [
                (x, y),
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]:
                if (
                    current_map[(new_x, new_y)]
                    or new_x < 0
                    or new_y < 0
                    or new_x >= size_x
                    or new_y >= size_y
                ):
                    continue
                next_positions.add((new_x, new_y))
        current_positions = next_positions
        current_map = perform_move(current_map, size_x, size_y)


def print_map(blizzard_map, size_x, size_y):
    for y in range(size_y):
        for x in range(size_x):
            if blizzard_map[(x, y)]:
                if len(blizzard_map[(x, y)]) > 1:
                    print("X", end="")
                else:
                    print(blizzard_map[(x, y)][0], end="")
            else:
                print(".", end="")
        print()


def part_1(blizzard_map, size_x, size_y, start_point, end_point):
    new_map, minutes = go_through_blizzard(
        blizzard_map, start_point, end_point, size_x, size_y
    )

    return minutes


def part_2(blizzard_map, size_x, size_y, start_point, end_point):
    new_map, to_end = go_through_blizzard(
        blizzard_map, start_point, end_point, size_x, size_y
    )
    new_map, to_start = go_through_blizzard(
        new_map, end_point, start_point, size_x, size_y
    )
    _, to_end_again = go_through_blizzard(
        new_map, start_point, end_point, size_x, size_y
    )

    return to_end + to_start + to_end_again + 2


size_x = len(raw_input[0])
size_y = len(raw_input)
start_point = (1, 0)
end_point = (size_x - 2, size_y - 1)

blizzard_map = defaultdict(list)
for y, line in enumerate(raw_input):
    for x, sign in enumerate(line):
        if sign != ".":
            blizzard_map[(x, y)].append(sign)

print("Part 1:", part_1(blizzard_map, size_x, size_y, start_point, end_point))
print("Part 2", part_2(blizzard_map, size_x, size_y, start_point, end_point))
