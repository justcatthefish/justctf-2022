# Port to which the task will be exposed
PORT=1337
IMAGE_NAME=pwn-darksols

cd private/darksols/

docker build \
    -t $IMAGE_NAME \
    -f Dockerfile \
    --build-arg FLAG='justCTF{if_y0u_m1ss_1t,_y0u_mu5t_b3_bl1nd!}' \
    .

docker rm -f $IMAGE_NAME
docker run -d \
    --name $IMAGE_NAME \
    --security-opt=no-new-privileges:true --user 1000:1000 --cap-drop=ALL \
    -p $PORT:8080 \
    $IMAGE_NAME
