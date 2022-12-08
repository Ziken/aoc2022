def part_1(raw_data: list[list[int]]) -> int:
    tree_map = [[0] * len(raw_data[0]) for _ in range(len(raw_data))]

    # horizontal
    for i, line in enumerate(raw_data):
        tree_map[i][0] += 1
        tree_map[i][-1] += 1
        max_tree_left = line[0]
        max_tree_right = line[-1]
        j = 1
        while j < len(raw_data):
            if max_tree_left < line[j]:
                tree_map[i][j] += 1
                max_tree_left = line[j]

            if max_tree_right < line[-j - 1]:
                tree_map[i][-j - 1] += 1
                max_tree_right = line[-j - 1]

            j += 1

    # vertical
    for i in range(len(raw_data)):
        tree_map[0][i] += 1
        tree_map[-1][i] += 1
        max_tree_up = raw_data[0][i]
        max_tree_down = raw_data[-1][i]
        j = 1
        while j < len(raw_data):
            if max_tree_up < raw_data[j][i]:
                tree_map[j][i] += 1
                max_tree_up = raw_data[j][i]

            if max_tree_down < raw_data[-j - 1][i]:
                tree_map[-j - 1][i] += 1
                max_tree_down = raw_data[-j - 1][i]

            j += 1

    result = 0
    for row in tree_map:
        result += len(list(filter(lambda x: x > 0, row)))

    return result


def part_2(raw_data: list[list[int]]):
    best_tree = 0
    for i, line in enumerate(raw_data):
        for j, current_height in enumerate(line):
            # right
            right_trees = 0
            for z in range(j + 1, len(line)):
                right_trees += 1
                if current_height <= line[z]:
                    break
            # left
            left_trees = 0
            for z in range(j - 1, -1, -1):
                left_trees += 1
                if current_height <= line[z]:
                    break
            # up
            up_trees = 0
            for z in range(i - 1, -1, -1):
                up_trees += 1
                if current_height <= raw_data[z][j]:
                    break
            # down
            down_trees = 0
            for z in range(i + 1, len(raw_data)):
                down_trees += 1
                if current_height <= raw_data[z][j]:
                    break

            r = right_trees * left_trees * up_trees * down_trees
            if r > best_tree:
                best_tree = r

    return best_tree


with open("08_input.txt") as f:
    raw_data = f.read().splitlines()
    raw_data: list[list[int]] = [list(map(int, line.strip())) for line in raw_data]

    print("Part 1:", part_1(raw_data))
    print("Part 2:", part_2(raw_data))

