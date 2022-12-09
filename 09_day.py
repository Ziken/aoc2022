def distance(x1, y1, x2, y2):
    a = (x1 - x2) ** 2 + (y1 - y2) ** 2
    return a


# with open("09_input_temp.txt") as f:
def get_coors(prev_x, prev_y, x, y):
    d = distance(prev_x, prev_y, x, y)
    if d > 8:
        print(d)

    if d == 4:
        if prev_x == x:
            if distance(prev_x, prev_y, x, y + 1) > distance(prev_x, prev_y, x, y - 1):
                return x, y - 1
            else:
                return x, y + 1
        if prev_y == y:
            if distance(prev_x, prev_y, x + 1, y) > distance(prev_x, prev_y, x - 1, y):
                return x - 1, y
            else:
                return x + 1, y
    if d == 5 or d == 8:
        possible_pos = [
            (x + 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y + 1),
            (x - 1, y - 1),
        ]
        min_i = 0
        for p in range(len(possible_pos)):
            if distance(prev_x, prev_y, *possible_pos[p]) < distance(
                prev_x, prev_y, *possible_pos[min_i]
            ):
                min_i = p

        return possible_pos[min_i]

    return x, y


def part_1(data):
    head_x = 0
    head_y = 0
    tail_x = 0
    tail_y = 0
    tail_moves = {(tail_x, tail_y)}
    for row in data:
        # print(row)
        # for y in range(4, -1, -1):
        #     for x in range(6):
        #         if x == head_x and y == head_y and x == tail_x and y == tail_y:
        #             print("H", end="")
        #         elif x == head_x and y == head_y:
        #             print("H", end="")
        #         elif x == tail_x and y == tail_y:
        #             print("T", end="")
        #         else:
        #             print('.', end="")
        #     print()
        #
        # print('-'*12)
        s = row.split()
        match s[0], int(s[1]):
            case "R", d:
                for _ in range(d):
                    head_x += 1
                    match distance(head_x, head_y, tail_x, tail_y):
                        case 4:
                            tail_x += 1
                            tail_moves.add((tail_x, tail_y))
                        case 5:
                            if head_y > tail_y:
                                tail_x += 1
                                tail_y += 1
                            else:
                                tail_x += 1
                                tail_y -= 1
                            tail_moves.add((tail_x, tail_y))
            case "U", d:
                for _ in range(d):
                    head_y += 1
                    match distance(head_x, head_y, tail_x, tail_y):
                        case 4:
                            tail_y += 1
                            tail_moves.add((tail_x, tail_y))
                        case 5:
                            if head_x > tail_x:
                                tail_x += 1
                                tail_y += 1
                            else:
                                tail_x -= 1
                                tail_y += 1
                            tail_moves.add((tail_x, tail_y))

            case "L", d:
                for _ in range(d):
                    head_x -= 1
                    match distance(head_x, head_y, tail_x, tail_y):
                        case 4:
                            tail_x -= 1
                            tail_moves.add((tail_x, tail_y))
                        case 5:
                            if head_y > tail_y:
                                tail_x -= 1
                                tail_y += 1
                            else:
                                tail_x -= 1
                                tail_y -= 1
                            tail_moves.add((tail_x, tail_y))
            case "D", d:
                for _ in range(d):
                    head_y -= 1
                    match distance(head_x, head_y, tail_x, tail_y):
                        case 4:
                            tail_y -= 1
                            tail_moves.add((tail_x, tail_y))
                        case 5:
                            if head_x > tail_x:
                                tail_x += 1
                                tail_y -= 1
                            else:
                                tail_x -= 1
                                tail_y -= 1
                            tail_moves.add((tail_x, tail_y))

    return len(tail_moves)


def part_2(data):
    # track every point of tail, one by one
    head_x = 0
    head_y = 0
    tails = [
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
    ]

    tail_moves = {(tails[-1][0], tails[-1][1])}
    for index, row in enumerate(data):
        s = row.split()
        match s[0], int(s[1]):
            case "R", d:
                for _ in range(d):
                    head_x += 1
                    prev_tail_x = head_x
                    prev_tail_y = head_y
                    for i in range(len(tails)):
                        x, y = get_coors(prev_tail_x, prev_tail_y, *tails[i])
                        tails[i][0] = x
                        tails[i][1] = y
                        prev_tail_x = tails[i][0]
                        prev_tail_y = tails[i][1]

                    tail_moves.add((tails[-1][0], tails[-1][1]))
            case "U", d:
                for _ in range(d):
                    head_y += 1
                    prev_tail_x = head_x
                    prev_tail_y = head_y
                    for i in range(len(tails)):
                        x, y = get_coors(prev_tail_x, prev_tail_y, *tails[i])
                        tails[i][0] = x
                        tails[i][1] = y
                        prev_tail_x = tails[i][0]
                        prev_tail_y = tails[i][1]

                    tail_moves.add((tails[-1][0], tails[-1][1]))
                    # tail_moves.add((tail_x, tail_y))

            case "L", d:
                for _ in range(d):
                    head_x -= 1
                    prev_tail_x = head_x
                    prev_tail_y = head_y
                    for i in range(len(tails)):
                        x, y = get_coors(prev_tail_x, prev_tail_y, *tails[i])
                        tails[i][0] = x
                        tails[i][1] = y
                        prev_tail_x = tails[i][0]
                        prev_tail_y = tails[i][1]

                    tail_moves.add((tails[-1][0], tails[-1][1]))
            case "D", d:
                for _ in range(d):
                    head_y -= 1
                    prev_tail_x = head_x
                    prev_tail_y = head_y
                    for i in range(len(tails)):
                        x, y = get_coors(prev_tail_x, prev_tail_y, *tails[i])
                        tails[i][0] = x
                        tails[i][1] = y
                        prev_tail_x = tails[i][0]
                        prev_tail_y = tails[i][1]

                    tail_moves.add((tails[-1][0], tails[-1][1]))

    return len(tail_moves)


with open("09_input.txt") as f:
    input = f.read().splitlines()
print("Part 1:", part_1(input))
print("Part 2:", part_2(input))


#
# print("asdf")
# print(distance(1, 1, 0, 0)) # 2
# print(distance(1, 1, 1, 0)) # 1
# print(distance(1, 1, 2, 0)) # 2
# print(distance(1, 1, 2, 1)) # 1
# print(distance(1, 1, 2, 2)) # 2
# print(distance(1, 1, 1, 2)) # 1
# print(distance(1, 1, 0, 2)) # 2
#
# print('sad')
# print(distance(2, 2, 1, 0)) # 5
# print(distance(2, 2, 2, 0)) # 4
# print(distance(2, 2, 3, 0)) # 5
# print(distance(2, 2, 0, 2)) # 4

# generate 2d  Cartesian as a comment
# (0, 0)
# (0, 1)
# (0, 2)

"""
== U 8 ==

.........
.........
.........
.........
.........
.........
.........
........H (9, 9)
........1
........2
........3
.......54
......6..
.....7...
....8....
...9..... (1, 1)

== L 8 ==

.........
.........
.........
.........
.........
.........
.........
H1234....
....5....
....6....
....7....
....8....
....9....
.........
.........
...s.....
"""

# print(distance(1, 4, 9, 9))  # 89
# print(distance(1, 4, 8, 9))  # 74
# print(distance(1, 4, 7, 9))  # 61
# print(distance(1, 4, 6, 9))  # 50
# print(distance(1, 4, 5, 9))  # 41
# print(distance(1, 4, 4, 9))  # 34
# print(distance(1, 4, 3, 9))  # 29
# print(distance(1, 4, 2, 9))  # 26
# print(distance(1, 4, 1, 9))  # 25

"""
......
......
......
....H.
4321..  (4 covers 5, 6, 7, 8, 9, s)

......
......
....H.
.4321.
......  (4 covers 5, 6, 7, 8, 9, s)


......
......
....H.
.4321.
5.....  (5 covers 6, 7, 8, 9, s)
"""
