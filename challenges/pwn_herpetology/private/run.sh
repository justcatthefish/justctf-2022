#!/bin/sh

# Port to which the task will be exposed
PORT=${1-37259}

cd private

IMG="pwn-herpetology"
docker build \
    --build-arg FLAG='justCTF{1earn_mor3_ab0ut_sn4kes_by_und3rfl0wing_st4ck}' \
    -t $IMG -f Dockerfile .

docker rm -f $IMG
docker run -d \
    --restart=always \
    --name $IMG \
    --security-opt=no-new-privileges:true --cap-drop=ALL \
    --read-only \
    -p $PORT:37259 \
    $IMG
