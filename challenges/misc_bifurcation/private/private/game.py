#!/usr/bin/env python
"""
Bifurcation is a game where you have to traverse a binary tree in order to find
the flag. Only one path through the tree gives you correct output.
"""

import math
import random
from dataclasses import dataclass
from typing import List, Tuple

from tree import Flag, Node, flag_root

# Tree part
# ============================================================

# ============================================================
# ============================================================

WALL = "#"
EMPTY = " "


@dataclass
class Pos:
    x: int
    y: int


@dataclass
class Board:
    width: int
    height: int

    _board: List[List[str]]

    def print(self):
        for row in self._board:
            print("".join(row))

    @classmethod
    def from_cols_and_rows(cls, cols, rows):

        B = []
        for r in range(1, rows):
            if r == 1:
                row = [WALL] * cols
            else:
                row = []

                for c in range(1, cols):
                    if c == 1:
                        row.append(WALL)
                    else:
                        row.append(EMPTY)
                else:
                    row.append(WALL)

            B.append(row)
        else:
            B.append([WALL] * cols)

        new = cls(cols, rows, B)
        return new

    def __getitem__(self, item):
        return self._board[item]


def board(width, height, difficulty) -> Board:
    # TODO: add mazes or other objects that make it harder to solve the larger
    # the maze
    return Board.from_cols_and_rows(width, height)


def randpos(board):
    pos = Pos(
        random.randrange(1, board.width - 1),
        random.randrange(1, board.height - 1),
    )
    return pos


def check(player, left, right, board):
    # Overlapping points
    playerXleft = player.x != left.x and player.y != left.y
    playerXright = player.x != right.x and player.y != right.y
    leftXright = left.x != right.x and left.y != right.y

    # playeroints overlapping with walls
    playerXwall = board[player.y][player.x] != WALL
    leftXwall = board[left.y][left.x] != WALL
    rightXwall = board[right.y][right.x] != WALL

    # check if all pass
    if all(
        [
            playerXleft,
            playerXright,
            leftXright,
            playerXwall,
            leftXwall,
            rightXwall,
        ]
    ):
        return True

    return False


def random_positions(board: Board):

    P = randpos(board)
    L = randpos(board)
    R = randpos(board)

    while not check(P, L, R, board):
        P = randpos(board)
        L = randpos(board)
        R = randpos(board)

    return P, L, R


class Keys:
    UP = "Wwk"
    DOWN = "Ssj"
    LEFT = "Aah"
    RIGHT = "Ddl"


def islegal(move, player: Pos, board: Board) -> bool:
    # Simplest way to check legality is to move and see if it's a wall

    y, x = player.y, player.x
    if move in Keys.UP and player.y > 1:
        y -= 1
    elif move in Keys.DOWN and player.y < board.height - 1:
        y += 1
    elif move in Keys.RIGHT and player.x < board.width - 1:
        x += 1
    elif move in Keys.LEFT and player.x > 1:
        x -= 1

    if board[y][x] == WALL:
        return False

    return True


def move(player: Pos, board: Board, step: str, node: Node, left: Pos, right: Pos):
    board[player.y][player.x] = EMPTY

    if step in Keys.UP and player.y > 1:
        player.y -= 1
    elif step in Keys.DOWN and player.y < board.height - 1:
        player.y += 1
    elif step in Keys.RIGHT and player.x < board.width - 1:
        player.x += 1
    elif step in Keys.LEFT and player.x > 1:
        player.x -= 1

    board[player.y][player.x] = "P"

    write_exits(board, node, left, right)


def write_exits(board: Board, node: Node, left, right):
    if node.L:
        board[left.y][left.x] = node.L.text
    if node.R:
        board[right.y][right.x] = node.R.text

    if node.L is None and node.R is None:
        print("Game Over :(")
        exit()


def write_player(board: Board, player: Pos):
    board[player.y][player.x] = "P"


def level(width, height, node, difficulty) -> Tuple[Node, str]:
    B = board(width, height, difficulty)
    P, L, R = random_positions(B)

    write_player(B, P)
    write_exits(B, node, L, R)

    while 1:
        B.print()
        steps = input("Your move!> ")
        for step in steps:
            if not islegal(step, P, B):
                print("Illegal move! Can't walk through walls")
                continue

            move(P, B, step, node, L, R)

        if P.y == L.y and P.x == L.x:
            print(f"You found `{node.L.text}`!")
            print("Moving to next level")
            return node.L, node.L.text

        if P.y == R.y and P.x == R.x:
            print(f"You found `{node.R.text}`!")
            print("Moving to next level")
            return node.R, node.R.text

    raise NotImplemented


def print_flag(found_flag):
    print(f"Current flag: {found_flag}")


def main():
    found_flag = ""
    node = flag_root

    # ========
    # TUTORIAL
    # ========
    print("Welcome to Bifurcation")
    print("This is a simple game. You're given a map, and your position P on the map")
    print("Your goal is to find the exit from the dungeon.")
    print("To move up you can use 'w' or 'k'")
    print("To move down you can use 's' or 'j'")
    print("To move left you can use 'a' or 'h'")
    print("To move right you can use 'd' or 'l'")
    print("-----")
    print("Your first task is to find `j`!")
    node, next_letter = level(5, 5, Flag.root, difficulty=None)
    found_flag += next_letter
    assert found_flag == "j"
    print_flag(found_flag)

    print("Great! You found first letter")
    print(
        "You can send more than one command at the time, for example 'www'"
        " will go up by three spots"
    )
    node, next_letter = level(7, 7, Flag.FIRST, difficulty=None)
    found_flag += next_letter
    assert found_flag == "ju"
    print_flag(found_flag)

    print("Yay! Two letters!")
    print(
        "You can also mix and match different letters, for example 'wasd' will"
        "move you by four spots but you will end up in the same place"
    )
    print("and `WAAWW` will go two spots left and three places up")
    node, next_letter = level(9, 9, Flag.SECOND, difficulty=None)
    found_flag += next_letter
    assert found_flag == "jus"
    print_flag(found_flag)

    print("As you can see on each step you're collecting letters")
    print("The ultimate goal of the game is to catch them all!")
    node, next_letter = level(12, 12, Flag.THIRD, difficulty=None)
    found_flag += next_letter
    assert found_flag == "just"
    print_flag(found_flag)

    print("However, you can also see the difficulty is going up")
    print("Sometimes you might find more than one exit – choose wisely!")
    node, next_letter = level(25, 15, Flag.FOURTH, difficulty=None)
    found_flag += next_letter
    assert found_flag == "justC"
    print_flag(found_flag)

    print(
        "You need to be very lucky when choosing your doors, only one of the"
        " paths, leads out of the dungeon"
    )
    node, next_letter = level(25, 5, Flag.FIFTH, difficulty=None)
    found_flag += next_letter
    assert found_flag == "justCT"
    print_flag(found_flag)

    print(
        "You will know you have the correct exit when you find the last"
        " relevant character"
    )
    node, next_letter = level(13, 37, Flag.SIXTH, difficulty=None)
    found_flag += next_letter
    assert found_flag == "justCTF"
    print_flag(found_flag)

    print("Good luck!")

    # ===========
    # Actual Game
    # ===========
    while 1:

        W = random.randrange(10, 13)
        H = random.randrange(5, 12)
        difficulty = math.sqrt(len(found_flag))

        node, next_letter = level(W, H, node, difficulty)
        found_flag += next_letter
        print_flag(found_flag)


if __name__ == "__main__":
    main()
