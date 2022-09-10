import socket
import sys
import subprocess
import json
import hashlib

from fastecdsa.point import Point
from secrets import randbits

from client_config import client_privkey_share

from frosty import mod_hash, generate_nonce, coords, Curve, N
from telnetlib import Telnet

HOSTPORT = sys.argv[1], int(sys.argv[2] if len(sys.argv) > 2 else 4444)

def read(tn : Telnet) -> dict:
    msg = tn.read_until(b"\n")
    return json.loads(msg)

def parse_ec(p):
    x, y = p
    return Point(int(x, 16), int(y, 16), Curve)

def write(tn : Telnet, msg : dict):
    tn.write(json.dumps(msg).encode() + b'\n')

HASHCASH_PREFIX = b'Please use the following command to solve the Proof of Work:'
BANNER = b'{"banner": "Welcome to Very Frosty\'s Snowman Signing Server. Choose an option: sign or verify"}'

def read_welcome_or_hashcash(tn):
    while True:
        d = tn.read_until(b'\n')
        print("Read line:", d)

        if HASHCASH_PREFIX in d:
            powstr = tn.read_until(b'\n')
            print("PoW:", powstr)
            out = subprocess.check_output(powstr.split())
            solvedpow = out.split(b'hashcash token: ')[-1]
            print("Sending solved PoW:", solvedpow)
            tn.write(solvedpow)
        elif BANNER in d:
            return

def sign_message(msg : bytes) -> (int, int):
    with Telnet(*HOSTPORTPORT) as tn:
        #welcome = read(tn)
        read_welcome_or_hashcash(tn)
        write(tn, {"op": "sign"})
        D = parse_ec(read(tn)["D"])
        (k, K) = generate_nonce()
        write(tn, {"D": coords(K), "msg":msg.hex()})
        z = int(read(tn)["z"], 16)
        c = mod_hash(msg, K + D)
        z1 = (k + client_privkey_share * c) % Curve.q
        return (z + z1) % Curve.q, c

def verify_message(msg : bytes, z : int, c : int) -> bool:
    with Telnet(*HOSTPORT) as tn:
        #welcome = read(tn)
        read_welcome_or_hashcash(tn)
        write(tn, {"op": "verify", "m":msg.hex(), "z":hex(z)[2:], "c":hex(c)[2:]})
        success = read(tn)["verified"]
        if success:
            print(read(tn)["flag"])
        return success

def session(msg : bytes):
    with Telnet(*HOSTPORT) as tn:
        #_ = read(tn)
        read_welcome_or_hashcash(tn)
        write(tn, {"op": "sign"})
        t = parse_ec(read(tn)["D"])
        rbar = randbits(N) % Curve.q, randbits(N) % Curve.q
        tbar = rbar[0]*Curve.G + t, rbar[1]*Curve.G + t
        cbar = mod_hash(msg, tbar[0]), mod_hash(msg, tbar[1])
        b = (yield (t, cbar))
        r = rbar[b]
        t = rbar[b]
        c = rbar[b]
        write(tn, {"D": coords(r * Curve.G), "msg": msg.hex()})
        z = read(tn)["z"]
    yield int(z, 16)

def rho(cs, xs, q):
    if type(xs[0]) == int:
        start = 0
    else:
        start = Point.IDENTITY_ELEMENT
    s = sum((pow(2, i, q) * pow(cs[i][1] - cs[i][0], -1, q) * xs[i] for i in range(len(cs))), start=start)
    if type(s) == int:
        s %= q
    return s


def forge(msg : bytes):
    sessions = [session(bytes([i])) for i in range(N)]
    ts_cs = [next(s) for s in sessions]
    ts = [t for (t, _) in ts_cs]
    cs = [c for (_, c) in ts_cs]
    t = rho(cs, ts, Curve.q)
    c = mod_hash(msg, t)
    d = (c - rho(cs, [cbar[0] for cbar in cs], Curve.q)) % Curve.q
    dbits = [int(b) for b in bin(d)[2:].rjust(N, '0')][::-1]
    zs = [s.send(dbits[i]) for i, s in enumerate(sessions)]
    z = (rho(cs, zs, Curve.q) + c * client_privkey_share) % Curve.q
    return (z, c)

if __name__ == "__main__":
    msg = b'Gimme!'
    (z, c) = forge(msg)
    assert verify_message(msg, z, c)
