#!/usr/bin/env bash

mkdir -p /tmp/web_gitara/flag/
mkdir -p /tmp/web_gitara/tmp/
cp -f flag.txt /tmp/web_gitara/flag/flag.txt

docker-compose -p web_gitara -f private/docker-compose.yml rm --force --stop
docker-compose -p web_gitara -f private/docker-compose.yml build
docker-compose -p web_gitara -f private/docker-compose.yml up -d
