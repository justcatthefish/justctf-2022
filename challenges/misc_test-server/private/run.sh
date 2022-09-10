#!/usr/bin/env bash

docker-compose -p misc_test-server -f private/docker-compose.yml rm --force --stop
docker-compose -p misc_test-server -f private/docker-compose.yml build
docker-compose -p misc_test-server -f private/docker-compose.yml up -d
