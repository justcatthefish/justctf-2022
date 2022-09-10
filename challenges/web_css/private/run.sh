#!/usr/bin/env bash

export FLAG=$(cat flag.txt)
export PASSWD=`cat /dev/urandom | tr -cd '[:alpha:]' | head -c48`
export SECRET_KEY=`cat /dev/urandom | tr -cd '[:alpha:]' | head -c48`

docker-compose -p web_css -f private/docker-compose.yml rm --force --stop
docker-compose -p web_css -f private/docker-compose.yml build
docker-compose -p web_css -f private/docker-compose.yml up


