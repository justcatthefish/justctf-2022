#!/usr/bin/env bash

# server not yet needed
if [[ ! -e /.CTF_SERVER ]]; then
    exit 0;
fi

mkdir -p /tmp/web_gohttpwin/

# share files server
python3 -m http.server -d /tmp/web_gohttpwin/ &
http_share="$!"

# build files
export FLAG=$(cat flag.txt)
docker build --build-arg "FLAG=$FLAG" -t app private
id=$(docker create app)
docker cp $id:/app.zip /tmp/web_gohttpwin/app.zip
docker rm -v $id

# run vagrant
cd ./private
vagrant up --provision

# close share files
kill -9 $http_share
