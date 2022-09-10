#!/usr/bin/env sh

cp ./flag.txt ./private/src/xml/flag.txt

cd ./private/src

docker-compose -p web_api_intended -f docker-compose.yml rm --force --stop
docker-compose -p web_api_intended -f docker-compose.yml build
docker-compose -p web_api_intended -f docker-compose.yml up -d
