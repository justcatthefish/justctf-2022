#!/usr/bin/env sh
exec socat TCP-LISTEN:5002,reuseaddr,fork,keepalive,keepidle=20,keepintvl=20,keepcnt=2 EXEC:'/pwn/socat-sigpipe-fixup timeout 3m /pwn/cli',nofork,su=pwn
