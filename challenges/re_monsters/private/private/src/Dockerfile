FROM ubuntu:21.10
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y libc++-dev libc++abi-dev clang make libunwind-dev

RUN groupadd ctf && \
    useradd -G ctf --home=/pwn pwn

WORKDIR /task
COPY ./. /task/.

RUN make

