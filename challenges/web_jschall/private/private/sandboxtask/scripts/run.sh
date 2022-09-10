#!/bin/bash

export FLAG=$(cat /flag.txt)
sed -i "s@listen 80;@listen 80; listen unix:/tmp/task/sock.unix;@g" /etc/nginx/nginx.conf
sed -i "s/FLAG_PLACEHOLDER/$FLAG/g" /etc/nginx/nginx.conf

/scripts/iptables.sh
service nginx restart

su -l justctf -pc '/home/justctf/app'
