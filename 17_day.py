import copy
from collections import defaultdict
from dataclasses import dataclass
from itertools import cycle

BOARD_LENGTH = 7


@dataclass
class Figure:
    positions: list[tuple[int, int]]
    max_left: int
    max_right: int
    global_id = 1

    def __init__(self, positions):
        self.positions = positions
        self.max_left = -min(positions, key=lambda x: x[0])[0]
        self.max_right = BOARD_LENGTH - 1 - max(positions, key=lambda x: x[0])[0]
        self.id = Figure.global_id
        Figure.global_id += 1

    def move_figure(self, x, y):
        return Figure([(x + dx, y + dy) for dx, dy in self.positions])

    @property
    def top(self):
        return max(self.positions, key=lambda x: x[1])[1]

    @property
    def bottom(self):
        return min(self.positions, key=lambda x: x[1])[1]


FIGURES = [
    (Figure([(2, 0), (3, 0), (4, 0), (5, 0)])),  # -
    (Figure([(3, 0), (2, 1), (3, 1), (4, 1), (3, 2)])),  # +
    (Figure([(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)])),  # _|
    (Figure([(2, 0), (2, 1), (2, 2), (2, 3)])),  # |
    (Figure([(2, 0), (3, 0), (2, 1), (3, 1)])),  # o
]


class Board:
    OFFSET = 4

    def __init__(self, jet: str):
        SIZE = 20000
        self.board: list[list[bool]] = [
            [False, False, False, False, False, False, False] for _ in range(SIZE)
        ]
        self.history_of_jet_ids = dict()
        self.history_of_figures = defaultdict(list)
        self.fig_i = 0
        self.start_y = 0
        self.jet = jet
        self.jet_i = 0

    def m(self) -> str:
        a = self.jet[self.jet_i]
        self.jet_i += 1
        if self.jet_i == len(self.jet):
            self.jet_i = 0

        return a

    def put_figure(self, figure):
        self.history_of_jet_ids[self.fig_i] = self.jet_i
        current_move = 0
        for _ in range(self.OFFSET):
            if self.m() == "<":
                current_move -= 1
                if current_move < figure.max_left:
                    current_move = figure.max_left
            else:
                current_move += 1
                if current_move > figure.max_right:
                    current_move = figure.max_right

        moved_figure = figure.move_figure(current_move, self.start_y)

        while True:
            potential_bottom_move = moved_figure.move_figure(0, -1)
            can_move = potential_bottom_move.bottom >= 0
            for x, y in potential_bottom_move.positions:
                if self.board[y][x]:
                    can_move = False
                    break

            if not can_move:
                break

            current_move = 0
            if self.m() == "<":
                current_move -= 1
                if current_move < potential_bottom_move.max_left:
                    current_move = potential_bottom_move.max_left
            else:
                current_move += 1
                if current_move > potential_bottom_move.max_right:
                    current_move = potential_bottom_move.max_right

            potential_jet_move = potential_bottom_move.move_figure(current_move, 0)
            can_move = True
            for x, y in potential_jet_move.positions:
                if self.board[y][x]:
                    can_move = False
                    break
            if can_move:
                moved_figure = potential_jet_move
            else:
                moved_figure = potential_bottom_move

        # apply position
        for x, y in moved_figure.positions:
            self.history_of_figures[y].append((self.fig_i, figure.id))
            if self.board[y][x] is not False:
                raise Exception("Collision")
            self.board[y][x] = figure.id

        if (moved_figure.top + 1) > self.start_y:
            self.start_y = moved_figure.top + 1

        self.fig_i += 1

    def print_board(self):
        # for row in reversed(self.board[2847+19: 2847+19 + 2702]):
        for row in reversed(self.board[:2500]):
            # for row in self.board[:5]:0
            for s in row:
                if s == 1:
                    print("=", end="")
                elif s == 2:
                    print("+", end="")
                elif s == 3:
                    print("J", end="")
                elif s == 4:
                    print("|", end="")
                elif s == 5:
                    print("o", end="")
                else:
                    print(".", end="")
            print()


def find_interval(board):
    intervals = []
    for main_index in range(2500):
        if len(intervals) > 500:
            break  # Found enough intervals

        find_rows = [board.board[main_index + i] for i in range(500)]
        for i in range(len(board.board)):
            found = True
            for j in range(len(find_rows)):
                if board.board[i + j] != find_rows[j]:
                    found = False
                    break
            if found and i != main_index:
                intervals.append(i)

    first_possible_interval = intervals[0]

    # There is a situation that the | element can get through the crack then this interval can be hard to repeat
    for possible_interval in range(
        first_possible_interval, first_possible_interval + 200
    ):
        prev_figure_id = max(
            board.history_of_figures[possible_interval], key=lambda x: x[0]
        )[0]
        is_good_interval = True
        for i in range(1, 11):
            current_figure_id = max(
                board.history_of_figures[possible_interval - i], key=lambda x: x[0]
            )[0]
            if abs(current_figure_id - prev_figure_id) > 2:
                is_good_interval = False
                break
            prev_figure_id = current_figure_id
        if is_good_interval:
            return possible_interval, intervals[1] - intervals[0]

    raise Exception("Could not find interval")


def get_rock_interval(start, end):
    figs = set()
    for i in range(start, end):
        for fig in board.history_of_figures[i]:
            figs.add(fig[0])

    return len(figs)


with open("17_input.txt") as f:
    jet = f.read().strip()
board = Board(jet)

for i, f in enumerate(cycle(FIGURES)):
    if i == 2022:
        print("Part 1:", board.start_y)

    if i == 10000:
        break

    board.put_figure(f)


start_interval, interval = find_interval(board)
b_start_figure = min(board.history_of_figures[start_interval], key=lambda x: x[0])
rocks_interval = get_rock_interval(start_interval, start_interval + interval)

tower_interval_height = interval
calculated_height = (
    (1000000000000 - b_start_figure[0]) // rocks_interval
) * tower_interval_height
rock_to_put = (1000000000000 - b_start_figure[0]) % rocks_interval

new_board = Board(jet)
new_board.jet_i = board.history_of_jet_ids[b_start_figure[0]]

figs = cycle(FIGURES)
# set proper figure start
for f in FIGURES:
    if f.id == b_start_figure[1]:
        break
    next(figs)

for i in range(rock_to_put):
    f = next(figs)
    new_board.put_figure(f)

print("Part 2:", (start_interval + calculated_height + new_board.start_y))
