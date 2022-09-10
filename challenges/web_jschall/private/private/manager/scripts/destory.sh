#!/bin/bash

set -ex
name="$1"

rm -rf "/tmp/web_jschall/$name/"
docker kill "sandbox_web_jschall_$name"