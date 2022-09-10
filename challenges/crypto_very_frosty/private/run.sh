#!/usr/bin/env sh
# Port to which the task will be exposed
PORT=4445

cd private/

IMAGE_NAME=crypto-very-frosty

docker build \
    -t $IMAGE_NAME \
    -f Dockerfile \
    .

docker rm -f $IMAGE_NAME
docker run -d \
    -e POW_CHALLENGE=1 \
    -e HASHCASH_DIFFICULT=16 \
    --name $IMAGE_NAME \
    --security-opt=no-new-privileges:true --cap-drop=ALL \
    -p $PORT:4445 \
    $IMAGE_NAME
