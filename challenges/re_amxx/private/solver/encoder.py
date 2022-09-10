from textwrap import wrap
from hashlib import sha256
from itertools import cycle
import sys

from decoder import decode

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


def encode(nick, passwd):
    return ''.join(map(lambda v: f'%04x' % v, stage3(stage2(stage1(passwd, nick)))))


def stage1(passwd, nick):
    xored = [a ^ b for a, b in zip(map(ord, passwd), cycle(map(ord, nick)))]
    for i in range(0, len(passwd), 2):
        if i + 1 >= len(passwd):
            break

        xored[i], xored[i + 1] = xored[i + 1], xored[i]

    return xored


def stage2(input):
    return [mapping[v] for v in input]


def stage3(input):
    b = 12314

    for i, c in enumerate(input):
        b += c * 0xDEAD
        b += 1
        b %= 0x1000
        input[i] = b

    return input


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print(encode(sys.argv[2], sys.argv[1]))
        exit(1)

    users = [
        ("Joe", "joejoejoejoe"),
        ("Botman", "q123123q"),
        ("Fragnatic", "passw0rd"),
        ("Campers Death", "hotdog87"),
        ("Headshot Deluxe", "winteriscoming"),
        ("Pr0g4m3r", "justCTF{4lm057_d34d_g4m3}"),
        ("L33t", "headshot"),
        ("Dredd", "awp420awp"),
        ("Rivit", "admin1337"),
        ("Wujek", "plgurom!"),
        ("shw", "topplayer"),
        ("rumcajs", "zaq1@WSX"),
        ("fex", "123123123")
    ]

    for u, p in users:
        enc = encode(u, p)
        print(f'{{"{u}", "{enc}"}},')
        print(decode(enc, u) == p)
