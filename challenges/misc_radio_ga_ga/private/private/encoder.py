#!/usr/bin/env python3

import sys

data = sys.argv[1]

PREFIX = "100000000"
VAL1 = "10000"
VAL0 = "100"
msg = PREFIX

for i in data:
    if i == "1":
        msg += VAL1
    elif i == "0":
        msg += VAL0
    else:
        exit(1)

#Dodaj 1 zeby oznaczyc koniec transmisji
msg += "1"    

print(msg)
exit(0)