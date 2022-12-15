import re
from collections import defaultdict


with open("15_input.txt") as f:
    raw_data = f.read().strip().splitlines()

line_regexp = re.compile(r"x=(-?\d+).+y=(-?\d+).+x=(-?\d+).+y=(-?\d+)")
sensor_beacons = []
for line in raw_data:
    sx, sy, bx, by = list(map(int, line_regexp.findall(line)[0]))
    sensor_beacons.append((sx, sy, bx, by))


def part_1(sensor_beacons):
    track_y = 2000000
    tracked_positions = set()

    for sx, sy, bx, by in sensor_beacons:
        size = abs(sx - bx) + abs(sy - by)

        distance = abs(abs(sy) - abs(track_y))
        if distance > size:
            continue

        points_length = 1 + 2 * (size - distance)
        start_x = sx - (size - distance)
        start_y = track_y

        for i in range(points_length):
            tracked_positions.add((start_x + i, start_y))

    for sx, sy, bx, by in sensor_beacons:
        if (sx, sy) in tracked_positions:
            tracked_positions.remove((sx, sy))
        if (bx, by) in tracked_positions:
            tracked_positions.remove((bx, by))

    return len(tracked_positions)


def _find_beacon(tracked_positions: dict[int, list[tuple[int, int]]]):
    for y, xs in tracked_positions.items():
        xs.sort(key=lambda y: y[0])
        rx1, rx2 = xs[0]
        for x1, x2 in xs[1:]:
            if rx2 < x1:
                return rx2 + 1, y

            if rx2 < x2:
                rx2 = x2

    raise ValueError("No beacon found")


def part_2(sensor_beacons):
    tracked_positions = defaultdict(list)
    for sx, sy, bx, by in sensor_beacons:
        size = abs(sx - bx) + abs(sy - by)

        for track_y in range(0, 4000000):
            distance = abs(abs(sy) - abs(track_y))
            if distance > size:
                continue

            points_length = 1 + 2 * (size - distance)
            start_x = sx - (size - distance)
            start_y = track_y

            tracked_positions[start_y].append((start_x, start_x + points_length - 1))

    beacon = _find_beacon(tracked_positions)
    return beacon[0] * 4000000 + beacon[1]


print("Part 1:", part_1(sensor_beacons))
print("Part 2:", part_2(sensor_beacons))
