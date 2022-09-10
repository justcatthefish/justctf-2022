#!/bin/bash

sed -i "s/FLAG_PLACEHOLDER/$FLAG/g" /etc/nginx/nginx.conf

/scripts/iptables.sh
service nginx restart

su -l justctf -pc '/home/justctf/app'
