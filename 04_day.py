import re


def part_1(file):
    fully_overlapped = 0
    for line in file:
        a1, a2, b1, b2 = list(map(int, re.split(r"[,-]", line.strip())))
        if a1 <= b1 <= b2 <= a2 or b1 <= a1 <= a2 <= b2:
            fully_overlapped += 1

    return fully_overlapped


def part_2(file):
    overlapped_count = 0
    for line in file:
        a1, a2, b1, b2 = list(map(int, re.split(r"[,-]", line.strip())))
        if a1 <= b1 <= a2 or a1 <= b2 <= a2 or b1 <= a1 <= b2 or b1 <= a2 <= b2:
            overlapped_count += 1

    return overlapped_count


with open("04_input.txt") as f:
    print("Part 1:", part_1(f))

with open("04_input.txt") as f:
    print("Part 2:", part_2(f))
