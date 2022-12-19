import datetime
import math
from collections import defaultdict

# raw_input = """
# 2,2,2
# 1,2,2
# 3,2,2
# 2,1,2
# 2,3,2
# 2,2,1
# 2,2,3
# 2,2,4
# 2,2,6
# 1,2,5
# 3,2,5
# 2,1,5
# 2,3,5
# """.strip().splitlines()

# raw_input = """
# 1,0,1
# 1,2,1
# 0,1,1
# 3,1,1
# 1,1,0
# 1,1,3
# """.strip().splitlines()

with open("18_input.txt") as f:
    raw_input = f.read().strip().splitlines()


CUBES = []
for line in raw_input:
    x, y, z = list(map(int, line.split(",")))
    CUBES.append((x, y, z))


def count_not_covered_walls(cubes):
    covered_walls_cubes = dict()
    for (x, y, z) in cubes:
        covered_walls_cubes[(x, y, z)] = 0

    for (x, y, z) in cubes:
        adjacent_cubes = [
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1),
        ]
        for cube in adjacent_cubes:
            if cube in covered_walls_cubes:
                covered_walls_cubes[cube] += 1
    not_covered = 0
    for covered_walls in covered_walls_cubes.values():
        not_covered += 6 - covered_walls

    return not_covered


def part_1():
    return count_not_covered_walls(CUBES)


def part_2():
    cubes = CUBES.copy()
    min_y = math.inf
    max_y = -math.inf
    min_x = math.inf
    max_x = -math.inf
    min_z = math.inf
    max_z = -math.inf
    for x, y, z in cubes:
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
        if z < min_z:
            min_z = z
        if z > max_z:
            max_z = z

    empty_cubes = defaultdict(lambda: 0)

    # Find empty cubes inside the drop

    for y in range(min_y - 1, max_y + 2):
        for z in range(min_z - 1, max_z + 2):
            is_inside = False
            possible_empty_cubes = []
            zz = []
            for x in range(min_x - 1, max_x + 2):
                is_empty_cube = (x, y, z) not in cubes
                if not is_inside:
                    if (x - 1, y, z) in cubes and is_empty_cube:
                        is_inside = True
                if is_inside:
                    if not is_empty_cube and (x - 1, y, z) not in cubes:
                        is_inside = False
                        # print('inside', possible_empty_cubes)
                        for c in possible_empty_cubes:
                            empty_cubes[c] += 1
                        possible_empty_cubes = []
                    else:
                        possible_empty_cubes.append((x, y, z))
                zz.append(is_inside)

    for x in range(min_x - 1, max_x + 2):
        for z in range(min_z - 1, max_z + 2):
            is_inside = False
            possible_empty_cubes = []
            for y in range(min_y - 1, max_y + 2):
                is_empty_cube = (x, y, z) not in cubes
                if not is_inside:
                    if (x, y - 1, z) in cubes and is_empty_cube:
                        is_inside = True
                if is_inside:
                    if not is_empty_cube and (x, y - 1, z) not in cubes:
                        is_inside = False
                        for c in possible_empty_cubes:
                            empty_cubes[c] += 1
                        # empty_cubes.extend(possible_empty_cubes)
                        possible_empty_cubes = []
                    else:
                        possible_empty_cubes.append((x, y, z))

    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            is_inside = False
            possible_empty_cubes = []
            for z in range(min_z - 1, max_z + 2):
                is_empty_cube = (x, y, z) not in cubes
                if not is_inside:
                    if (x, y, z - 1) in cubes and is_empty_cube:
                        is_inside = True
                if is_inside:
                    if not is_empty_cube and (x, y, z - 1) not in cubes:
                        is_inside = False
                        for c in possible_empty_cubes:
                            empty_cubes[c] += 1
                        possible_empty_cubes = []
                    else:
                        possible_empty_cubes.append((x, y, z))

    # Used for faster finding cracks in the drop
    crack_visited_false = set()
    for y in range(min_y - 1, max_y + 2):
        for z in range(min_z - 1, max_z + 2):
            for x in range(min_x - 1, max_x + 2):
                is_empty_cube = (x, y, z) not in cubes
                if not is_empty_cube:
                    crack_visited_false.add((x, y, z))
                else:
                    break
                for x in range(max_x + 2, min_x - 2, -1):
                    is_empty_cube = (x, y, z) not in cubes
                    if not is_empty_cube:
                        crack_visited_false.add((x, y, z))
                    else:
                        break

    for i, c in enumerate(empty_cubes):
        if empty_cubes[c] < 3:
            crack_visited_false.add(c)

    # Eliminate any crack in the drop
    for i, c in enumerate(empty_cubes):
        print(i, len(empty_cubes))
        if empty_cubes[c] == 3:
            is_c = is_crack(
                c,
                set(),
                crack_visited_false,
                min_x - 1,
                max_x + 1,
                min_y - 1,
                max_y + 1,
                min_z - 1,
                max_z + 1,
            )
            if not is_c:
                cubes.append(c)

    return count_not_covered_walls(cubes)


def is_crack(
    cube, visited: set, was_crack: set, min_x, max_x, min_y, max_y, min_z, max_z
):
    if cube in was_crack:
        return True

    if cube in visited or cube in CUBES:
        return False

    x, y, z = cube
    if x < min_x or x > max_x:
        was_crack.update(visited)
        return True
    if y < min_y or y > max_y:
        was_crack.update(visited)
        return True
    if z < min_z or z > max_z:
        was_crack.update(visited)
        return True

    adjacent_cubes = [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]
    visited.add(cube)
    for c in adjacent_cubes:
        if is_crack(c, visited, was_crack, min_x, max_x, min_y, max_y, min_z, max_z):
            return True

    return False


print("Part 1:", part_1())
# Can take over 6 minutes
print("Part 2:", part_2())
