import math

with open("12_input.txt") as f:
    data = f.read().strip().splitlines()


def traverse_heatmap(heatmap, heatmap_distances, x, y, steps=0):
    if heatmap[y][x] == "S":
        curr = ord("a")
    elif heatmap[y][x] == "E":
        heatmap_distances[y][x] = steps
        return x, y
    else:
        curr = ord(heatmap[y][x])

    if steps >= heatmap_distances[y][x]:
        return None
    else:
        heatmap_distances[y][x] = steps

    possible_pos = []
    if x > 0:
        possible_pos.append((x - 1, y))
    if x < len(heatmap[y]) - 1:
        possible_pos.append((x + 1, y))
    if y > 0:
        possible_pos.append((x, y - 1))
    if y < len(heatmap) - 1:
        possible_pos.append((x, y + 1))

    routes = []

    for possible_x, possible_y in possible_pos:
        c = heatmap[possible_y][possible_x]
        if c == "E":
            c = "z"

        if ord(c) <= curr + 1:
            routes.append(
                traverse_heatmap(
                    heatmap, heatmap_distances, possible_x, possible_y, steps + 1
                )
            )

    for r in routes:
        if r:
            return r


def part_1():
    start_point = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "S":
                start_point = [x, y]
                break
    end_route = traverse_heatmap(data, heatmap_distances, *start_point)
    return heatmap_distances[end_route[1]][end_route[0]]


def part_2():
    start_points = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "S" or data[y][x] == "a":
                start_points.append([x, y])

    routes = []
    for i, s in enumerate(start_points):
        end_route = traverse_heatmap(data, heatmap_distances, *s)
        if end_route:
            routes.append(heatmap_distances[end_route[1]][end_route[0]])
    return min(routes)


heatmap_distances = [[math.inf] * len(data[0]) for y in range(len(data))]

print("Part 1:", part_1())
print("Part 2:", part_2())
