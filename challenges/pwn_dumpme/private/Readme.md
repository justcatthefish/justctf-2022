# dumpme

This task demonstrates that restricting ptrace to register values is pointless, and can be bypassed by faking syscalls.
Which in turn implies that execute-only almost always implies the read+execute permissions.
