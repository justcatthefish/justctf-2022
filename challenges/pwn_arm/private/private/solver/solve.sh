#!/usr/bin/env sh

if [ "$#" -le 1 ]; then
    echo "Use: <host> <port>"
    exit 1
fi

docker build -t solver-pwn-arm .
docker run --rm -it \
    --security-opt=no-new-privileges --cap-drop=ALL --user 1000:1000 \
    --network=host \
    solver-pwn-arm \
    /solve.py HOST="$1" PORT="$2" $*
