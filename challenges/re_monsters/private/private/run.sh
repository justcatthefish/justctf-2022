#!/usr/bin/env sh
exec socat -d -d TCP-LISTEN:1337,reuseaddr,fork,keepalive,keepidle=20,keepintvl=20,keepcnt=2 EXEC:'/task/socat-sigpipe-fixup unshare -Upf timeout 8m /task/monsters',nofork,su=pwn
#exec socat -d -d TCP-LISTEN:1337,reuseaddr,fork,keepalive,keepidle=20,keepintvl=20,keepcnt=2 EXEC:'/task/monsters',nofork,su=pwn
