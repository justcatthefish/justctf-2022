from aux import *
import sys

'''
justCTF2022
~ Tacet
'''

def single(i):
    e, p, Me, s = next(i)
    print("e = ", e)
    print("p = ", p)
    print("M**e mod p = ")
    print(Me)

    print("We expect you to provide sum(M % p) - sum of all elements in M % p.")
    us = int(input("sum: "))
    if us != s:
        print("Nope, we expected: ", s)
        exit(1)
    else:
        print("ok")

if __name__ == "__main__":
    sys.setrecursionlimit(10**6)
    for i in range(100):
        print(i, " / ", 100)
        single(i)

    print("justCTF{basic_math_just_fundametals}")
