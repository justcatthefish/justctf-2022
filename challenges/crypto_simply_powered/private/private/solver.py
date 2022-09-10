from aux import *
from pwn import connect
import sys 

'''
justCTF2022
~ Tacet
'''

con = connect("simply-powered-ams3.nc.jctf.pro", 4444)

def solve(Me, e, p):
    n = Me.shape[0]
    o = ord(n, p)
    assert gcd(o, e) == 1

    ie = mod_inverse(e, o)
    M = fp(Me, ie, p)

    return str(sum(M))

def read():
    con.readuntil("e =")
    e = int(con.readline())
    con.readuntil("p =")
    p = int(con.readline())
    con.readline()
    Me = eval(con.readline())


    return Me, e, p

def single():
    Me, e, p = read()
    con.sendline(solve(Me, e, p))

sys.setrecursionlimit(10**6)

for i in range(100):
    print("i = ", i)
    single()
con.interactive()

