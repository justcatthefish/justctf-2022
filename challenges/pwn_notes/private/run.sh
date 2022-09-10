#!/usr/bin/env sh

# Port to which the task will be exposed
PORT=${1-5001}

cp flag.txt ./private/flag.txt
cd private

IMG="pwn-notes"
docker build -t $IMG -f Dockerfile .


# Note: we add setuid/sys_admin to be able to change uid for unshare operation in socat
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
    -p $PORT:5001 \
    $IMG


