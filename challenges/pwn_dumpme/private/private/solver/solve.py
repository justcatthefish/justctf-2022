#!/usr/bin/env python3

from pwn import *

# Locally on MacOS use: PROXY=host.docker.internal
if args.PROXY:
    info("SETTING PROXY: " + args.PROXY)
    context.proxy = args.PROXY

with remote(args.HOST, args.PORT) as p:
    solver_bin = b64e(read('/pwn')).encode()

    N=64
    p.sendline(b'cd /tmp')

    info("SENDING DATA")
    for i in range(0, len(solver_bin), N):
        data = solver_bin[i:i+N]
        p.sendline(b"echo %s>>x" % data)
    info("SENT ALL DATA")

    p.sendline(b"cat x|base64 -d > y")
    p.sendline(b"chmod +x y")

    info("Now executing: /tmp/y /task/dumpme")

    p.sendline(b"/tmp/y /task/dumpme")

    print(p.recv())
    p.sendline(b"exit")
    print(p.recv())

    #p.interactive()
