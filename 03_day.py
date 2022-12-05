import string

PRIORITY_VALUE = {l: ord(l) - ord("a") + 1 for l in string.ascii_lowercase}
PRIORITY_VALUE.update({l: ord(l) - ord("A") + 1 + 26 for l in string.ascii_uppercase})


def part_1(file):
    sum_of_priority = 0
    for line in file:
        line = line.strip()
        first_seg, second_set = set(line[: len(line) // 2]), set(line[len(line) // 2 :])

        sum_of_priority += PRIORITY_VALUE[(first_seg & second_set).pop()]

    return sum_of_priority


def part_2(file):
    sum_of_priority = 0
    num_of_elves = 3
    while True:
        common_item = set(PRIORITY_VALUE.keys())
        for _ in range(num_of_elves):
            line = file.readline().strip()
            if not line:
                return sum_of_priority
            common_item &= set(line)
        sum_of_priority += PRIORITY_VALUE[common_item.pop()]


with open("03_input.txt") as file:
    print("Part 1:", part_1(file))

with open("03_input.txt") as file:
    print("Part 2:", part_2(file))
