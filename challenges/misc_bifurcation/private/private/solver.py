import subprocess as sp
import time
from collections import deque
from subprocess import PIPE, STDOUT
from typing import Optional

EmptyBoard = object()

DELAY = 0.0001


class Found(Exception):
    ...


def clean_line(line: bytes):
    return "".join([x for x in line if x == "#"])


def read_until_board(p, line):
    line = clean_line(line)
    board = [line]
    while 1:
        line = p.stdout.readline().decode()
        if line.startswith("###"):
            # Append the very last line with the border
            board.append(line.strip())
            return board

        board.append(line.strip())


def pb(board):
    for b in board:
        print("PB: ", b)


def path(P, t):
    _, *t = t
    trace = []

    if P[0] > t[0]:
        trace.append("w" * abs(P[0] - t[0]))
    if P[0] < t[0]:
        trace.append("s" * abs(P[0] - t[0]))
    if P[1] < t[1]:
        trace.append("d" * abs(P[1] - t[1]))
    if P[1] > t[1]:
        trace.append("a" * abs(P[1] - t[1]))

    return trace


def locate(board) -> tuple[tuple[int, int], list[tuple[str, int, int]]]:
    P = tuple()
    targets = []
    for r, row in enumerate(board):
        for c, ch in enumerate(row):
            if ch == "P":
                P = r, c

            elif ch.isalnum() or ch in "{}":
                targets.append((ch, r, c))

    return P, targets


def solve_board(board, target=None):
    P, targets = locate(board)

    if targets == []:
        return

    for t in targets:
        if target:
            if t[0] == target:
                # Return path to first target only, for debugging
                return "".join(path(P, t))
        else:
            # If not target, just return the first one.
            return "".join(path(P, t))


def run(host: Optional[str], port: str, prefix: list[str], until="") -> tuple[Optional[list[str]], Optional[list[str]]]:
    cmd = ["nc", host, port]
    if host is None:
        cmd = ["./game.py"]
    p = sp.Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    flag = ""
    moves = 1000
    last_char = None

    while moves > 0:
        moves -= 1
        # Read stdin line by line
        line = p.stdout.readline().decode().strip()
        # print("DEBUG: ", line)

        if "Game Over" in line or "Traceback" in line:
            if flag:
                print("FOUND FLAG: ", flag)
            print("FOUND DEAD END")
            return None, None

        # Find the beginning of the board.
        if line.startswith("###"):
            # Then switch to reading board mode until you read the entire board
            # (again, defined by the '###' at the end)
            board = read_until_board(p, line)

            # Once read, print the board
            # pb(board)
            if prefix:
                pref = prefix.pop(0)
                solution = solve_board(board, target=pref)
            else:
                _, letters = locate(board)
                return [x[0] for x in letters]

            if not solution:
                return None, None

            # NEVER FORGET TO ADD \n :<
            p.stdin.write(solution.encode() + b"\n")
            p.stdin.flush()
            time.sleep(DELAY)

            # And go back to the reading, but assume that you need to read next
            # line first
            continue

        if "You found `" in line.strip():
            _, last_char, _ = line.strip().split("`")
            if last_char == "}":
                raise Found(flag + last_char)

        if "Current flag" in line.strip():
            _, flag = line.split(":")
            flag = flag.strip()
            continue

    return None, None


def main(host: Optional[str], port: str):
    Q = deque()
    Q.append(list("justCTF"))

    while Q:
        q = Q.popleft()
        print(q)
        ab = run(host, port, q[:])
        if len(ab) == 1:
            [a] = ab
            b = None
        else:
            a, b = ab

        if a is not None:
            Q.append(q + [a])
        if b is not None:
            Q.append(q + [b])


if __name__ == "__main__":
    import argparse
    par = argparse.ArgumentParser()
    par.add_argument("host", default="bifurcation.nc.jctf.pro", nargs='?')
    par.add_argument("port", default="31789", nargs='?')
    arg = par.parse_args()
    # arg.host = None
    main(arg.host, arg.port)
