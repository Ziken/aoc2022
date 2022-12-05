import copy
import re
from collections import defaultdict


def part_1(input_data: dict[int, list], instructions: list[list[int]]):
    data = copy.deepcopy(input_data)
    for amount, from_move, to_move in instructions:
        while amount >= 0:
            data[to_move].append(data[from_move].pop())
            amount -= 1

    output = ""
    for key in sorted(data.keys()):
        output += data[key][-1]

    return output


def part_2(input_data, instructions: list[list[int]]):
    data = copy.deepcopy(input_data)
    for amount, from_move, to_move in instructions:
        data[to_move].extend(data[from_move][-(amount + 1) :])
        data[from_move][-(amount + 1) :] = []

    output = ""
    for key in sorted(data.keys()):
        output += data[key][-1]

    return output


cargo_crane = defaultdict(list)
instructions = []
with open("05_input.txt") as f:
    for line in f:
        for i, cargo in enumerate(line):
            if cargo.isalpha():
                cargo_crane[i // 4].insert(0, cargo)
        if line.strip() == "":
            break

    for line in f:
        instructions.append(list(map(lambda x: int(x) - 1, re.findall(r"[\d]+", line))))

    print(part_1(cargo_crane, instructions))
    print(part_2(cargo_crane, instructions))
