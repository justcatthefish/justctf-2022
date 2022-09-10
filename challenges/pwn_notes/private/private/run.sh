#!/usr/bin/env sh
exec socat TCP-LISTEN:5001,reuseaddr,fork,keepalive,keepidle=20,keepintvl=20,keepcnt=2 EXEC:'/pwn/socat-sigpipe-fixup unshare -Upf timeout 2m /pwn/notes',stderr,nofork,su=pwn
