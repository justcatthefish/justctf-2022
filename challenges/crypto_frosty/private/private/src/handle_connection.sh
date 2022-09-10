#!/usr/bin/env sh

set -ex

cd ./src

timeout 2m ./clihashcash_amd64
timeout 2m python3 ./frosty.py
