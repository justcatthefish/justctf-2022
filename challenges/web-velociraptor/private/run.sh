#!/usr/bin/env bash

mkdir -p /tmp/web_velociraptor/flag/
cp -f flag.txt /tmp/web_velociraptor/flag/flag.txt
chmod a+r /tmp/web_velociraptor/flag/flag.txt

docker-compose -p web_velociraptor -f private/docker-compose.yml rm --force --stop
docker-compose -p web_velociraptor -f private/docker-compose.yml build
docker-compose -p web_velociraptor -f private/docker-compose.yml up -d