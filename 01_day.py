def part_1(file):
    max_count = 0
    current_count = 0
    for line in file:
        if line.strip().isnumeric():
            current_count += float(line)
        else:
            if current_count > max_count:
                max_count = current_count
            current_count = 0

    return max_count


def part_2(file):
    keep_max_count = 3
    max_counts = []
    current_count = 0
    for line in file:
        if line.strip().isnumeric():
            current_count += float(line)
        else:
            max_counts.append(current_count)
            current_count = 0

    return sum(sorted(max_counts, reverse=True)[:keep_max_count])


with open("01_input.txt") as f:
    print("Part 1:", part_1(f))

with open("01_input.txt") as f:
    print("Part 2:", part_2(f))
