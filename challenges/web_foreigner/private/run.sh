#!/usr/bin/env bash

# server not yet needed
if [[ ! -e /.CTF_SERVER ]]; then
    exit 0;
fi

rm -rf /tmp/web_foreigner/;
mkdir -p /tmp/web_foreigner/;
chmod 777 /tmp/web_foreigner/;

export FLAG=$(cat flag.txt)

nerdctl compose -p web_baby-xsleak -f private/docker-compose.yml rm -f --stop
nerdctl compose -p web_baby-xsleak -f private/docker-compose.yml build
nerdctl compose -p web_baby-xsleak -f private/docker-compose.yml up -d
