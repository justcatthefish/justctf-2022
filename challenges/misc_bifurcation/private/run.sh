# Port to which the task will be exposed
PORT=31789

# insret flag here
# cp -f ./flag.txt ./private/
cd private/

IMAGE_NAME=misc-bifurcation

# Flag generated with shortuuid.random()[:14]
docker build \
    -t $IMAGE_NAME \
    -f Dockerfile \
    .

docker rm -f $IMAGE_NAME
docker run -d \
    --read-only \
    --name $IMAGE_NAME \
    --security-opt=no-new-privileges:true --user 1000:1000 \
    --cap-drop=ALL \
    --cap-add=CAP_SETUID \
    --cap-add=CAP_SETGID \
    -e flag='justCTF{uCA8ysuM8q9BTp}' \
    -p $PORT:8080 \
    $IMAGE_NAME
