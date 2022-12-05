from enum import Enum


class OpponentMove(str, Enum):
    ROCK = "A"
    PAPER = "B"
    SCISSORS = "C"


class PlayerMove(str, Enum):
    ROCK = "X"
    PAPER = "Y"
    SCISSORS = "Z"


class Outcome(str, Enum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"


LOSE_RPS_RULES = {
    OpponentMove.ROCK: PlayerMove.PAPER,
    OpponentMove.SCISSORS: PlayerMove.ROCK,
    OpponentMove.PAPER: PlayerMove.SCISSORS,
}

WIN_RPS_RULES = {
    OpponentMove.PAPER: PlayerMove.ROCK,
    OpponentMove.ROCK: PlayerMove.SCISSORS,
    OpponentMove.SCISSORS: PlayerMove.PAPER,
}

MOVE_POINTS = {
    PlayerMove.ROCK.name: 1,
    PlayerMove.PAPER.name: 2,
    PlayerMove.SCISSORS.name: 3,
}

WIN_POINTS = 6
DRAW_POINTS = 3
LOSE_POINTS = 0


def part_1(file):
    score = 0
    for round in file:
        opponent_move, player_move = round.strip().split(" ")

        if LOSE_RPS_RULES[opponent_move] == player_move:
            score += WIN_POINTS
        elif PlayerMove(player_move).name == OpponentMove(opponent_move).name:
            score += DRAW_POINTS
        else:
            score += LOSE_POINTS

        score += MOVE_POINTS[PlayerMove(player_move).name]

    return score


def part_2(file):
    score = 0
    for round in file:
        opponent_move, outcome = round.strip().split(" ")

        if outcome == Outcome.WIN:
            score += WIN_POINTS
            score += MOVE_POINTS[LOSE_RPS_RULES[opponent_move].name]
        elif outcome == Outcome.DRAW:
            score += DRAW_POINTS
            score += MOVE_POINTS[OpponentMove(opponent_move).name]
        elif outcome == Outcome.LOSE:
            score += LOSE_POINTS
            score += MOVE_POINTS[WIN_RPS_RULES[opponent_move].name]

    return score


with open("02_input.txt") as file:
    print("Part 1:", part_1(file))

with open("02_input.txt") as file:
    print("Part 2:", part_2(file))
