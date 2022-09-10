#!/usr/bin/env sh
cd /task
exec socat TCP-LISTEN:8080,reuseaddr,fork,keepalive,keepidle=20,keepintvl=20,keepcnt=2 EXEC:'timeout 9m ./game.py',stderr,nofork
