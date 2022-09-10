from z3 import *
from textwrap import wrap
from hashlib import sha256
from itertools import cycle
import sys

mapping = {}
order = 0
for i in range(0x100):
    if len(mapping) == 0x100: continue

    s = f'%08x' % i
    hash = sha256(s.encode()).hexdigest()
    for p in map(lambda v: int(v, 16), wrap(hash, 2)):
        if p not in mapping:
            mapping[p] = order
            order += 1

reverse_mapping = {v: k for k, v in mapping.items()}


def stage1(input, nick):
    dexored = [a ^ b for a, b in zip(input, cycle(map(ord, nick)))]
    password = ''.join(map(chr, dexored))
    return password


def stage2(input, nick):
    revmapped_input = [reverse_mapping[v] for v in input]

    for i in range(0, len(revmapped_input), 2):
        if i + 1 >= len(revmapped_input):
            break

        revmapped_input[i], revmapped_input[i + 1] = revmapped_input[i + 1], revmapped_input[i]

    return stage1(revmapped_input, nick)


def stage3(nick, encoded):
    out = []
    start_value = 12314
    output_ints = list(map(lambda v: int(v, 16), wrap(encoded, 4)))
    xs = BitVecs(' '.join([f'x{i}' for i in range(len(output_ints))]), 8)
    s = Solver()
    for v, expected in zip(xs, output_ints):
        start_value += v * 0xDEAD
        start_value += 1
        start_value %= 0x1000
        s.add(start_value == expected)

    while True:
        if s.check() == sat:
            recovered = [s.model()[v].as_long() for v in xs]
            out.append(stage2(recovered, nick))
            s.add(Or([s.model()[v].as_long() != v for v in xs]))
        else:
            break

    return out


def decode(nick, passwd_encoded):
    return stage3(nick, passwd_encoded)[0]


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("python decode.py nick passwd_hash")
        exit(1)

    dec = decode(sys.argv[2], sys.argv[1])
    print(dec)
