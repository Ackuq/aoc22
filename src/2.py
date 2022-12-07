from enum import Enum
from typing import List

from utils import get_input


class Move(Enum):
    Rock = "rock"
    Paper = "paper"
    Scissor = "scissor"


player1 = {"A": Move.Rock, "B": Move.Paper, "C": Move.Scissor}

shape_score = {Move.Rock: 1, Move.Paper: 2, Move.Scissor: 3}

player2 = {"X": Move.Rock, "Y": Move.Paper, "Z": Move.Scissor}

rules = {Move.Rock: Move.Scissor, Move.Paper: Move.Rock, Move.Scissor: Move.Paper}
inv_rules = {value: key for key, value in rules.items()}


def main(input: List[str]) -> None:
    score = 0
    for line in input:
        p1_str, p2_str = line.strip().split(" ")
        p1 = player1[p1_str]
        p2 = player2[p2_str]
        # Add shape score
        current = shape_score[p2]
        if p2 is rules[p1]:
            # P1 wins
            current += 0
        elif p1 is rules[p2]:
            # P2 wins
            current += 6
        else:
            # draw
            current += 3
        score += current

    print(f"Score {score}")

    score = 0
    for line in input:
        p1_str, outcome = line.strip().split(" ")
        p1 = player1[p1_str]
        if outcome == "X":
            # Need to lose
            current = 0
            p2 = rules[p1]
        elif outcome == "Y":
            # Need to end in draw
            current = 3
            p2 = p1
        else:
            # Need to win
            current = 6
            p2 = inv_rules[p1]
        current += shape_score[p2]
        score += current
    print(f"Part 2: {score}")


if __name__ == "__main__":
    main(get_input(2))
