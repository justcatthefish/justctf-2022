#!/usr/bin/env bash

rm -rf /tmp/web_symple-unzipper/;
mkdir -p /tmp/web_symple-unzipper/;
chmod 777 /tmp/web_symple-unzipper/;

export FLAG=$(cat flag.txt)

docker-compose -p web_symple-unzipper -f private/docker-compose.yml rm --force --stop
docker-compose -p web_symple-unzipper -f private/docker-compose.yml build
docker-compose -p web_symple-unzipper -f private/docker-compose.yml up -d
