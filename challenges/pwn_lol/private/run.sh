# Port to which the task will be exposed
PORT=1337
IMAGE_NAME=pwn-leagueoflamports

cd private/LeagueOfLamports/

docker build \
    -t $IMAGE_NAME \
    -f Dockerfile \
    --build-arg FLAG="justCTF{All_towers_fall_it's_just_what_they_do_when_I'm_4r0und}" \
    .

# NOTE:
# The options below are generally INSECURE. We use them as we use nsjail anyway.
# Docker is used just for easier bootstraping of nsjail, i.e.:
# - to have a non-host chroot (and consistent environment) for jailed processes/tasks
# - to be able to run task with one command, assuming docker is installed on machine
#
# We need:
# - CHOWN, SETUID, SETGID, AUDIT_WRITE - to use `su -l jailed ...`
# - SYS_ADMIN and CHOWN to prepare (mount) cgrops for nsjail
# - no apparmor and no seccomp to prepare cgroups and to spawn jails
#

# YOLO
docker rm -f $IMAGE_NAME
docker run \
    -d \
    --name $IMAGE_NAME \
    -p $PORT:8080 \
    --security-opt=no-new-privileges:true --user 1000:1000 --cap-drop=ALL \
    $IMAGE_NAME
