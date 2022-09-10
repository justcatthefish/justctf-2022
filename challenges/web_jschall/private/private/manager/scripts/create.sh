#!/bin/bash

set -ex
name="$1"
# stop_timeout="$2"

mkdir -p "/tmp/shared/$name/"
chmod 777 "/tmp/shared/$name/"

docker run \
  -d \
  -v /tmp/web_jschall/$name/:/tmp/task/ \
  -v /tmp/web_jschall/flag.txt:/flag.txt:ro \
  --rm \
  --name "sandbox_web_jschall_$name" \
  sandboxtask

echo "1" > "/tmp/shared/$name/server.pid"