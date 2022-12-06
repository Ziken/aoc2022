def solution(data, range_chars):
    for i in range(len(data)):
        part = data[i : i + range_chars]
        if len(set(part)) == range_chars:
            return i + range_chars


with open("06_input.txt") as f:
    data = f.read().strip()
    print("Part 1:", solution(data, 4))
    print("Part 2:", solution(data, 14))
