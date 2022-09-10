#!/usr/bin/env sh

echo "$#"

if [ "$#" -l 2 ]; then
    echo "Use: <host> <port>"
    exit 1
fi

IMG="solver-pwn-skilltest"
cp ../skilltest .
cp ../libc-2.34.so .
docker build -t $IMG .
docker rm -f $IMG
docker run --rm -it \
    --name $IMG \
    --security-opt=no-new-privileges --cap-drop=ALL --user 1000:1000 \
    --network=host \
    solver-pwn-skilltest \
    /solver/solve.py REMOTE HOST="$1" PORT="$2" $*
