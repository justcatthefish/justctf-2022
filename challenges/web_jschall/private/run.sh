#!/usr/bin/env bash

rm -rf /tmp/web_jschall/;
mkdir -p /tmp/web_jschall/;
chmod 777 /tmp/web_jschall/;

export FLAG=$(cat flag.txt)

docker-compose -p web_jschall -f private/docker-compose.yml rm --force --stop
docker-compose -p web_jschall -f private/docker-compose.yml build
docker-compose -p web_jschall -f private/docker-compose.yml up -d
