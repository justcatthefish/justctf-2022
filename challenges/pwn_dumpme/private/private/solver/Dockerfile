FROM ziglang/static-base:llvm13-x86_64-1 as solverbin

COPY pwn.c /
RUN /deps/local/bin/zig build-exe -fno-stack-check -lc -target x86_64-linux-musl -O ReleaseSmall --strip pwn.c


FROM disconnect3d/pwntools:ubuntu22.04-pwntools
COPY --from=solverbin /pwn /pwn
COPY solve.py /solve.py

