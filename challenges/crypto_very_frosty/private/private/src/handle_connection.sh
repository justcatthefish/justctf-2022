#!/usr/bin/env bash

set -ex

cd ./src

if [[ ! -z "$POW_CHALLENGE" ]]; then
    timeout 1m ./clihashcash_amd64
fi
timeout 10m python3 ./frosty.py
