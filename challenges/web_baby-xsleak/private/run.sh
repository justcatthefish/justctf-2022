#!/usr/bin/env bash

export DOCKER_BUILDKIT=1
rm -rf /tmp/web_baby-xsleak/;
mkdir -p /tmp/web_baby-xsleak/;
chmod 777 /tmp/web_baby-xsleak/;

export FLAG=$(cat flag.txt)

#nix build ./private/bot/#defaultPackage.x86_64-linux
#docker load < ./result
#
#nix build ./private/app/#defaultPackage.x86_64-linux
#docker load < ./result

docker-compose -p web_baby-xsleak -f private/docker-compose.yml rm --force --stop
docker-compose -p web_baby-xsleak -f private/docker-compose.yml build
docker-compose -p web_baby-xsleak -f private/docker-compose.yml up -d
