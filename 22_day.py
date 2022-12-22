import re
from enum import Enum


class MapSign(str, Enum):
    ROAD = "."
    WALL = "#"
    EMPTY = " "
    MAP_END = "\n"


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


DIRECTION_SCORE = {
    Direction.RIGHT: 0,
    Direction.DOWN: 1,
    Direction.LEFT: 2,
    Direction.UP: 3,
}


def get_next_pos_on_map(current_pos, direction):
    possible_x, possible_y = current_pos
    if direction == Direction.UP:
        possible_y -= 1
    elif direction == Direction.RIGHT:
        possible_x += 1
    elif direction == Direction.DOWN:
        possible_y += 1
    elif direction == Direction.LEFT:
        possible_x -= 1

    return possible_x, possible_y


def get_possible_next_pos_on_map(board, current_pos, direction: Direction):
    counter = 0
    while True:
        counter += 1
        possible_x, possible_y = get_next_pos_on_map(current_pos, direction)
        if possible_x < 0:
            possible_x = len(board[current_pos[1]]) - 1
        if possible_x >= len(board[current_pos[1]]):
            possible_x = 0
        if possible_y < 0:
            possible_y = len(board) - 1
        if possible_y >= len(board):
            possible_y = 0

        if board[possible_y][possible_x] == MapSign.ROAD:
            return possible_x, possible_y

        if board[possible_y][possible_x] == MapSign.WALL:
            return None, None  # End of the current path

        current_pos = (possible_x, possible_y)

    return possible_x, possible_y


def get_direction(current_direction: Direction, turn: str):
    if turn == "L":
        return Direction((current_direction.value - 1) % 4)
    elif turn == "R":
        return Direction((current_direction.value + 1) % 4)
    else:
        raise ValueError("Invalid turn")


def part_1(board, start_position, start_direction, board_path):
    copy_board = board.copy()

    # make regular width
    max_width = max(len(line) for line in copy_board)
    for i, line in enumerate(copy_board):
        copy_board[i] = line.ljust(max_width, MapSign.EMPTY)

    current_direction = start_direction
    current_pos = start_position
    for i in range(1, len(board_path), 2):
        current_direction = get_direction(current_direction, board_path[i - 1])
        path_length = int(board_path[i])

        for _ in range(path_length):
            next_pos = get_possible_next_pos_on_map(
                copy_board, current_pos, current_direction
            )
            if next_pos[0] is None:
                break
            current_pos = next_pos

    return (
        (current_pos[0] + 1) * 4
        + (current_pos[1] + 1) * 1000
        + DIRECTION_SCORE[current_direction]
    )


def get_square_id(square_width, current_pos, prev_square=None):
    """
      1122
      1122
      33
      33
    5544
    5544
    66
    66
    """
    x = current_pos[0]
    y = current_pos[1]
    if 0 <= x < square_width:
        if 0 <= y < square_width:
            return 5
        if square_width <= y < 2 * square_width:
            if prev_square == 5:
                return 3
            if prev_square == 3:
                return 5
        if 2 * square_width <= y < 3 * square_width:
            return 5
        elif 3 * square_width <= y < 4 * square_width:
            return 6
        elif y >= 4 * square_width:
            return 2
    if square_width <= x < 2 * square_width:
        if y < 0:
            return 6
        if 0 <= y < square_width:
            return 1
        elif square_width <= y < 2 * square_width:
            return 3
        elif 2 * square_width <= y < 3 * square_width:
            return 4
        if 3 * square_width <= y < 4 * square_width:
            if prev_square == 4:
                return 6
            if prev_square == 6:
                return 4

    if 2 * square_width <= x < 3 * square_width:
        if y < 0:
            return 6
        if 0 <= y < square_width:
            return 2
        if square_width <= y < 2 * square_width:
            if prev_square == 2:
                return 3
            if prev_square == 3:
                return 2
        if 2 * square_width <= y < 3 * square_width:
            return 2
    elif x >= 3 * square_width:
        return 4
    elif x < 0:
        if 2 * square_width <= y < 3 * square_width:
            return 1
        elif 3 * square_width <= y < 4 * square_width:
            return 1

    return -1


def get_next_pos_on_square(square_width, current_pos, direction):
    next_x, next_y = get_next_pos_on_map(current_pos, direction)
    current_square = get_square_id(square_width, current_pos)
    next_square = get_square_id(square_width, (next_x, next_y), current_square)
    if current_square == next_square:
        return next_x, next_y, direction

    if current_square == 1:
        if next_square in (2, 3):
            return next_x, next_y, direction
        elif next_square == 5:
            return 0, 3 * square_width - next_y - 1, Direction.RIGHT
        elif next_square == 6:
            return 0, 3 * square_width + next_x - square_width, Direction.RIGHT
        else:
            raise ValueError("Invalid square")
    if current_square == 2:
        if next_square == 1:
            return next_x, next_y, direction
        elif next_square == 3:
            return 2 * square_width - 1, next_x - square_width, Direction.LEFT
        elif next_square == 4:
            return 2 * square_width - 1, 3 * square_width - next_y - 1, Direction.LEFT
        elif next_square == 6:
            return next_x - 2 * square_width, 4 * square_width - 1, Direction.UP
        else:
            raise ValueError("Invalid square")
    if current_square == 3:
        if next_square in (1, 4):
            return next_x, next_y, direction
        elif next_square == 2:
            return square_width + next_y, square_width - 1, Direction.UP
        elif next_square == 5:
            return next_y - square_width, 2 * square_width, Direction.DOWN
        else:
            raise ValueError("Invalid square")
    if current_square == 4:
        if next_square in (3, 5):
            return next_x, next_y, direction
        if next_square == 6:
            return square_width - 1, 2 * square_width + next_x, Direction.LEFT
        if next_square == 2:
            return 3 * square_width - 1, 3 * square_width - next_y - 1, Direction.LEFT
    if current_square == 5:
        if next_square in (4, 6):
            return next_x, next_y, direction
        if next_square == 3:
            return square_width, square_width + next_x, Direction.RIGHT
        if next_square == 1:
            return square_width, 3 * square_width - next_y - 1, Direction.RIGHT
    if current_square == 6:
        if next_square == 5:
            return next_x, next_y, direction
        if next_square == 4:
            return next_y - 2 * square_width, 3 * square_width - 1, Direction.UP
        if next_square == 2:
            return 2 * square_width + next_x, 0, Direction.DOWN
        if next_square == 1:
            return next_y - 2 * square_width, 0, Direction.DOWN

    return None


def get_possible_next_pos_on_square(
    board, current_pos, direction: Direction, square_width
):
    possible_x, possible_y, direction = get_next_pos_on_square(
        square_width, current_pos, direction
    )

    if board[possible_y][possible_x] == MapSign.ROAD:
        return possible_x, possible_y, direction

    if board[possible_y][possible_x] == MapSign.WALL:
        return None, None, None  # End of the current path

    raise ValueError("Invalid map sign")


def part_2(board, start_position, start_direction, board_path):
    copy_board = board.copy()
    square_width = len(board_map) // 4
    current_direction = start_direction
    current_pos = start_position
    for i in range(1, len(board_path), 2):
        current_direction = get_direction(current_direction, board_path[i - 1])
        path_length = int(board_path[i])

        for _ in range(path_length):
            next_x, next_y, next_direction = get_possible_next_pos_on_square(
                copy_board, current_pos, current_direction, square_width
            )
            if next_x is None:
                break
            current_pos = (next_x, next_y)
            current_direction = next_direction

    return (
        (current_pos[0] + 1) * 4
        + (current_pos[1] + 1) * 1000
        + DIRECTION_SCORE[current_direction]
    )


board_map = []
with open("22_input.txt") as f:
    for line in f:
        if line == "\n":
            break
        board_map.append(line.rstrip())

    board_path = re.findall(r"([A-Z]+|\d+)", next(f))

current_pos = (0, 0)
current_direction = Direction.UP
board_path.insert(0, "R")

for i, sign in enumerate(board_map[0]):
    if sign == MapSign.ROAD:
        current_pos = (i, 0)
        break

print("Part 1:", part_1(board_map, current_pos, current_direction, board_path))
print("Part 2:", part_2(board_map, current_pos, current_direction, board_path))
