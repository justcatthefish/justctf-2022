with open('monsters','rb') as f:
    x = f.read()

flag = b"justCTF{l3aki1ng_str}"
fake_flag = b"justWTF{flag_here!@#}"

assert len(flag) == len(fake_flag)

x = x.replace(flag, fake_flag)

with open('monsters-public','wb') as f:
    f.write(x)
