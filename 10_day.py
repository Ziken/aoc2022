def part_1(data):
    def _check_s(s: int, x: int) -> int:
        if (s - 20) % 40 == 0:
            return s * x

    current_signal = 0
    strengths = []
    current_x = 1
    for instruction in data:
        match instruction.split(" "):
            case ["noop"]:
                current_signal += 1
                if s := _check_s(current_signal, current_x):
                    strengths.append(s)
            case ["addx", x]:
                current_signal += 1
                if s := _check_s(current_signal, current_x):
                    strengths.append(s)
                current_signal += 1
                if s := _check_s(current_signal, current_x):
                    strengths.append(s)
                current_x += int(x)

    return sum(strengths)


def part_2(data):
    def _check_s(s: int, pos: int) -> str:
        if (s % 40) in [pos - 1, pos, pos + 1]:
            return "#"
        return "."

    current_signal = 0
    sprite_pos = 1
    current_x = 1
    screen = []
    for instruction in data:
        match instruction.split(" "):
            case ["noop"]:
                current_signal += 1
                if s := _check_s(current_signal, sprite_pos):
                    screen.append(s)
            case ["addx", x]:
                current_signal += 1
                if s := _check_s(current_signal, sprite_pos):
                    screen.append(s)
                current_signal += 1
                if s := _check_s(current_signal, sprite_pos):
                    screen.append(s)
                current_x += int(x)
                sprite_pos = current_x + 1

    for i in range(0, len(screen), 40):
        print("".join(screen[i : i + 40]))


with open("10_input.txt") as f:
    raw_data = f.read().splitlines()
    print(part_1(raw_data))
    part_2(raw_data)
