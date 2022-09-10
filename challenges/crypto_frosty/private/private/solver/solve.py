import socket
import json
import hashlib
import subprocess

from fastecdsa.point import Point
from secrets import randbits

from frosty import mod_hash, generate_nonce, coords, Curve, N, parse_ec
from telnetlib import Telnet
import sys

HOSTPORT = sys.argv[1], int(sys.argv[2] if len(sys.argv) > 2 else 4444)

HASHCASH_PREFIX = b'Please use the following command to solve the Proof of Work:'
BANNER = b'''{"banner": "Welcome to Frosty's Snowman Signing Server. Choose an option: genkey, sign or verify"}'''

def read(tn : Telnet) -> dict:
    msg = tn.read_until(b"\n")
    return json.loads(msg)

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
        

def write(tn : Telnet, msg : dict):
    tn.write(json.dumps(msg).encode() + b'\n')

def forge(tn, msg : bytes) -> (Point, int, int):
    #welcome = read(tn)
    read_welcome_or_hashcash(tn)
    write(tn, {"op": "genkey"})
    server_share = parse_ec(read(tn)["pubkey_share"])
    sk, client_share = generate_nonce()
    Y = client_share - server_share
    write(tn, {"pubkey_share":coords(Y)})
    read(tn)
    k, K = generate_nonce()
    c = mod_hash(msg, K)
    z = (k + sk * c) % Curve.q
    return (client_share, z, c)


def verify_message(tn, msg : bytes, Y : Point, z : int, c : int) -> bool:
    welcome = read(tn)
    write(tn, {"op": "verify", "pubkey":coords(Y), "m":msg.hex(), "z":hex(z)[2:], "c":hex(c)[2:]})
    success = read(tn)["verified"]
    if (success):
        print(read(tn)["flag"])
    return success

if __name__ == "__main__":
    with Telnet(*HOSTPORT) as tn:
        msg = b'Gimme!'
        (Y, z, c) = forge(tn, msg)
        assert verify_message(tn, msg, Y, z, c)
