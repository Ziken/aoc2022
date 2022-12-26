from typing import Optional


def from_snafu_to_dec(snafu: str) -> int:
    num = 0
    for i, sign in enumerate(reversed(snafu)):
        if sign == "0":
            continue
        elif sign == "1":
            num += 5**i
        elif sign == "2":
            num += 5**i * 2
        elif sign == "-":
            num -= 5**i
        elif sign == "=":
            num -= 5**i * 2
    return num


def _snafu_converter_help(
    current_number: int, final_number: int, current_snafu: str, i: int
) -> Optional[str]:
    if current_number == final_number:
        return current_snafu
    if i < 0:
        return None

    if n3 := _snafu_converter_help(
        current_number, final_number, current_snafu + "0", i - 1
    ):
        return n3

    if current_number < final_number:
        if n1 := _snafu_converter_help(
            current_number + 5**i, final_number, current_snafu + "1", i - 1
        ):
            return n1

        if n2 := _snafu_converter_help(
            current_number + 5**i * 2, final_number, current_snafu + "2", i - 1
        ):
            return n2

    if current_number > final_number:
        n = _snafu_converter_help(
            current_number - 5**i, final_number, current_snafu + "-", i - 1
        )
        if n:
            return n
    if current_number > final_number:
        n = _snafu_converter_help(
            current_number - 5**i * 2, final_number, current_snafu + "=", i - 1
        )
        if n:
            return n


def from_dec_to_snafu(number: int) -> str:
    from_power = 0
    while 5**from_power < number and 5**from_power * 2 < number:
        from_power += 1

    for i in range(-4, 3, 1):
        if n := _snafu_converter_help(0, number, "", from_power + i):
            if from_snafu_to_dec(n) == number:
                return n
            if from_snafu_to_dec(n + "0") == number:
                return n + "0"


with open("25_input.txt") as f:
    raw_input = f.read().strip().splitlines()

result = 0
for line in raw_input:
    result += from_snafu_to_dec(line)

print("Part 1:", from_dec_to_snafu(result))
