FROM ubuntu:21.10
#FROM disconnect3d/nsjail:3.1-6483728

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y python3 python3-pip

RUN groupadd ctf && \
    useradd -G ctf --home=/pwn pwn

WORKDIR /task

RUN python3 -m pip install sympy

# If we want to build (note: sources are not available for participants)
#COPY ./src /task/src
#RUN cd /task/src && make && cp monsters /task/ && cd /task
COPY ./. .
COPY run.sh .

# Helper/fixer for socat issues
#COPY socat-sigpipe-fixup /task/socat-sigpipe-fixup
#RUN chmod 111 /task/socat-sigpipe-fixup && \
#    chmod 700 /task/run.sh

RUN apt update && apt install -y socat
RUN groupadd -g 99999 jailed && \
    useradd --uid 99999 --gid 99999 jailed && \
    mkdir /home/jailed && \
    chown jailed /home/jailed -R && \
    chmod 755 /home/jailed -R

USER 99999

CMD "/task/run.sh"
