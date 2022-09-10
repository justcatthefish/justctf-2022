#!/usr/bin/env python3

import sys

data = sys.argv[1]

PREFIX = "100000000"
VAL1 = "10000"
VAL0 = "100"

index = 0
msg = ""

while index < len(data):
    if data[index:].find(PREFIX) == 0:
        index += len(PREFIX)
    elif data[index:].find(VAL1) == 0:
        msg += "1"
        index += len(VAL1)
    elif data[index:].find(VAL0) == 0:
        msg += "0"
        index += len(VAL0)
    elif data[index:] == "1":
        index += 1
    else:
        exit(1)
    
print(msg)
exit(0)