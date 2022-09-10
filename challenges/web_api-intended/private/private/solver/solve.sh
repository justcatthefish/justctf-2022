#!/usr/bin/env sh

if [ "$#" -ne 2 ]; then
    echo "Use: <host> <port=80>"
    exit 1
fi

IMG=web_api_solver
docker rm -f $IMG

set -ex
docker build -t $IMG .

docker run --rm -it \
    --security-opt=no-new-privileges:true --user 1000:1000 --cap-drop=ALL \
    --network=host \
    $IMG \
    python3 solve.py $1 $2
