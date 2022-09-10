#!/usr/bin/env sh

# Port to which the task will be exposed
PORT=${1-5002}

cp flag.txt ./private/flag.txt
cd private

# register binfmt_misc handlers
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

IMG="pwn-arm"
docker build -t $IMG -f Dockerfile .

docker rm -f $IMG
docker run -d \
    --restart=always \
    --name $IMG \
    --read-only \
    --security-opt=no-new-privileges:true \
    --cap-drop=ALL \
    --cap-add=CAP_SETUID \
    --cap-add=CAP_SETGID \
    --cap-add=CAP_SYS_ADMIN \
    -p $PORT:5002 \
    $IMG
