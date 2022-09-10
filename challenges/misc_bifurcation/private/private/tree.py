import random
import os
from dataclasses import dataclass
from typing import Optional

random.seed(0x21337deadbeef)

@dataclass
class Node:
    """ """

    text: str
    L: Optional["Node"] = None
    R: Optional["Node"] = None

    @staticmethod
    def rand(excl):
        az = "abcdefghijklmnopqrstuvwxyz"
        az += az.upper()
        az = set(az)
        # Subtract the player as well
        az -= {"p", "P"}
        az -= set(excl)
        return random.choice(list(az))


def write(node, string: str) -> Node:
    """Returns root of a new tree"""
    # Once the string is empty just return
    if string:
        tx, string = string[0], string[1:]
        # Can simply and always assign to the left, because we later randomise
        # the position on 2d anyway.
        node.L = Node(text=tx)
        write(node.L, string)

        node.R = Node(text=Node.rand(excl=tx))
        write(node.R, "".join(Node.rand(excl=tx) for _ in string))

    return node


# prefix = "justCTF{"
# content = "B1n4rYTreeLoL"
# suffix = "}"
# flag = prefix + content + suffix
flag = os.environ["flag"]
_, flag_content = flag.split("{")


class Flag:
    # It's easier to make the tutorial with an empty root
    root = Node("")
    FIRST = root.L = j = Node("j")
    SECOND = j.L = u = Node("u")
    THIRD = u.L = s = Node("s")
    FOURTH = s.L = t = Node("t")

    FIFTH = t.L = C = Node("C")
    t.R = X = Node("X")

    SIXTH = C.L = T = Node("T")
    C.R = Y = Node("Y")

    SEVENTH = T.L = F = Node("F")
    T.R = Z = Node("Z")

    F.L = start = Node("{")


# NOTE: we can write this once, pickle, and then load again.
# Or we need to set a stable seed
flag_root = write(Flag.start, flag_content)


def find(node, flag, char: str):
    """
    Finds path through the binary tree until it finds the character
    """
    flag += node.text
    if node.text == char:
        return flag

    if node.L:
        gg = find(node.L, flag, char)
        if gg is not None:
            return gg

    if node.R:
        gg = find(node.R, flag, char)
        if gg is not None:
            return gg

    return None
