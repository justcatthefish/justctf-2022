from typing import List
from pwn import u32, u16, u8, p32, p16, p8
import sys
from dataclasses import dataclass

from decoder import decode

# File format:
# VAULT_MAGIC (int32)
# VAULT_VERSION (int16)
# ENTRIES (int32)
# [
#  stamp (int32)
#  keylen (int8)
#  vallen (int16)
#  key ([])
#  val ([])
#  ]
from encoder import encode


@dataclass
class NVaultEntry:
	stamp: int
	keylen: int
	vallen: int
	key: str
	val: str

@dataclass
class NVault:
	magic: int
	version: int
	entries_num: int
	entries: List[NVaultEntry]

class NVaultUtil:
	def __init__(self, path):
		self.path = path

	def read_all(self):
		with open(self.path, "rb") as f:
			magic = u32(f.read(4))
			ver = u16(f.read(2))
			entries = u32(f.read(4))
			entries_list = []
			for _ in range(entries):
				stamp = u32(f.read(4))
				keylen = u8(f.read(1))
				vallen = u16(f.read(2))
				key = f.read(keylen).decode()
				val = f.read(vallen).decode()
				entries_list.append(NVaultEntry(stamp, keylen, vallen, key, val))

		return NVault(magic, ver, entries, entries_list)

	def save(self, new_data):
		with open(self.path, "wb") as f:
			f.write(p32(new_data.magic))
			f.write(p16(new_data.version))
			f.write(p32(new_data.entries_num))
			for e in new_data.entries:
				f.write(p32(e.stamp))
				f.write(p8(e.keylen))
				f.write(p16(e.vallen))
				f.write(e.key.encode())
				f.write(e.val.encode())



if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("python nvault.py [read|patch] path")
		exit(1)

	read = sys.argv[1] == 'read'
	path = sys.argv[2]
	
	nvault = NVaultUtil(path)
	nvault_data = nvault.read_all()
	if read:
		for e in nvault_data.entries:
			print(f'{e.key}: {e.val} {decode(e.key, e.val)}')
	else:
		print("Before patch")
		for e in nvault_data.entries:
			print(f'{e.key}: {e.val} {decode(e.key, e.val)}')

		for i, e in enumerate(nvault_data.entries):
			if e.key == 'Pr0g4m3r':
				e.val = encode(e.key, "justCTF{4lm057_d34d_g4m3}")
				e.vallen = len(e.val)

		print("After patch")
		for e in nvault_data.entries:
			print(f'{e.key}: {e.val} {decode(e.key, e.val)}')

		nvault.save(nvault_data)
