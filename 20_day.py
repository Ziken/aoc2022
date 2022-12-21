class Number:
    def __init__(self, num):
        self.n = num

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Number({self.n})"

    def __eq__(self, other):
        if isinstance(other, int):
            return self.n == other

        return super().__eq__(other)


def mix_nums(nums, native_order_nums):
    length = len(nums)

    for num in native_order_nums:
        pos = nums.index(num)

        if num.n > 0:
            # end_pos = num.n
            end_pos = num.n
            while end_pos >= length:
                end_pos = (end_pos % length) + (end_pos // length)

            i = 0
            while i < end_pos:
                p1 = (pos + i) % length
                p2 = (pos + i + 1) % length
                if (pos + i) == length:
                    nums.insert(0, nums.pop())
                    end_pos += 1
                else:
                    nums[p1], nums[p2] = nums[p2], nums[p1]
                i += 1

            if p2 == 0:
                nums.insert(0, nums.pop())

        elif num.n < 0:
            i = 0
            end_pos = (abs(num.n) % length) + (abs(num.n) // length)
            while end_pos >= length:
                end_pos = (end_pos % length) + (end_pos // length)

            p2 = 0
            while i < end_pos:
                p1 = (pos - i) % length
                p2 = (pos - i - 1) % length
                if p1 == 0:
                    nums.append(nums.pop(0))
                    end_pos += 1
                else:
                    nums[p1], nums[p2] = nums[p2], nums[p1]
                i += 1
            if p2 == 0:
                nums.append(nums.pop(0))


def part_1(numbers: list[Number]) -> int:
    native_order_nums = numbers[:]
    nums = numbers[:]
    mix_nums(nums, native_order_nums)

    length = len(numbers)
    first_0 = nums.index(0)
    return sum(
        [
            nums[(1000 + first_0) % length].n,
            nums[(2000 + first_0) % length].n,
            nums[(3000 + first_0) % length].n,
        ]
    )


def part_2(numbers: list[Number]):
    nums = [Number(num.n * 811589153) for num in numbers]
    native_order_nums = nums[:]
    for i in range(10):
        mix_nums(nums, native_order_nums)

    length = len(numbers)
    first_0 = nums.index(0)
    return sum(
        [
            nums[(1000 + first_0) % length].n,
            nums[(2000 + first_0) % length].n,
            nums[(3000 + first_0) % length].n,
        ]
    )


nums = [
    1,
    2,
    -3,
    3,
    -2,
    0,
    4,
]
with open("20_input.txt") as f:
    nums = list(map(int, f.read().splitlines()))

input_numbers = [Number(num) for num in nums]

print("Part 1:", part_1(input_numbers))
print("Part 2:", part_2(input_numbers))
