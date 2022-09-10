FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive 

#RUN apt update && apt install gcc gdb git -yy
#RUN git clone https://github.com/pwndbg/pwndbg && cd pwndbg && ./setup.sh
#RUN pip3 install pwn

RUN apt update && apt install socat gcc -yy
RUN mkdir /pwn

# UNCOMMENT FOR REBUILDING
# NOTE: It may cause the chall to be not solvable or the solver to not work
#COPY notes.c /pwn/notes.c
#RUN gcc -fstack-clash-protection -fpie -Wl,-pie -Wl,-z,relro -fstack-protector-all -D_FORTIFY_SOURCE=2 -O2 -o /pwn/notes /pwn/notes.c && rm /pwn/notes.c

COPY notes /pwn/notes
COPY flag.txt /pwn/flag.txt
COPY run.sh /pwn/run.sh

RUN groupadd ctf && \
    useradd -G ctf --home=/pwn pwn

# Helper/fixer for socat issues
COPY socat-sigpipe-fixup /pwn/socat-sigpipe-fixup
RUN chmod 111 /pwn/socat-sigpipe-fixup && \
    chmod 700 /pwn/run.sh

CMD "/pwn/run.sh"
