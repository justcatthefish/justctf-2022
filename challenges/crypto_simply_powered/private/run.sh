#!/usr/bin/env sh
# Port to which the task will be exposed
PORT=4444

cd private/

IMAGE_NAME=crypto-simply-powered

docker build \
    -t $IMAGE_NAME \
    -f Dockerfile \
    .

docker rm -f $IMAGE_NAME
docker run -d \
    --name $IMAGE_NAME \
    --security-opt=no-new-privileges:true --cap-drop=ALL \
    -p $PORT:4444 \
    $IMAGE_NAME
