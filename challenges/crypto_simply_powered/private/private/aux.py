from sympy import mod_inverse, Matrix, gcd
from random import randint
import sympy 

'''
justCTF2022
~ Tacet
'''

def fp(M, n, p):
    if n <= 2:
        return (M**n)%p

    if n%2 == 1:
        return ( M * fp(M, n-1, p) ) %p
    else:
        H = fp(M, n//2, p)
        return H**2 % p


def ord(n, p):
    mul = 1
    for i in range(0, n):
        mul *= (p**n - p**i)

    return mul

def random_matrix(n, p):
    def random_matrix_impl(n, p):
        return Matrix([ [ randint(1, p-1) for _ in range(n)] for __ in range(n)])
    M = random_matrix_impl(n, p)
    while M.det() == 0:
        M = random_matrix_impl(n, p)

    return M

def find_e(n, p):
    o = ord(n, p)
    r = randint(2, o-1)

    while gcd(o, r) != 1:
        r = randint(2, o-1)

    return r

def prep_challenge(n, p):
    M = random_matrix(n, p)
    e = find_e(n, p)

    return fp(M, e, p), e, sum(M)

def get_n(i):
    if i < 50:
        return 2
    if i < 75:
        return 3
    if i < 98:
        return 7

    return 11

def get_p(i):
    if i == 7:
        return sympy.ntheory.generate.nextprime(randint(10**9, 10**10))

    if i < 50:
        return sympy.ntheory.generate.nextprime(randint(5, 100))

    if i < 80:
        return sympy.ntheory.generate.nextprime(randint(100, 1000))

    return sympy.ntheory.generate.nextprime(randint(10, 10**10))

def next(i):
    n =  get_n(i)
    p = get_p(i)
    Me, e, s = prep_challenge(n, p)

    return e, p, Me, s
