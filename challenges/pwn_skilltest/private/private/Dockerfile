FROM disconnect3d/nsjail:3.1-6483728

RUN groupadd -g 99999 jailed && \
    useradd --uid 99999 --gid 99999 jailed && \
    mkdir /home/jailed && \
    chown jailed /home/jailed -R && \
    chmod 755 /home/jailed -R

RUN mkdir -p /task

# Copy files
COPY skilltest ld-linux-x86-64.so.2 libc-2.34.so /task/
COPY nsjail.cfg run_task.sh flag.txt /

WORKDIR /task
RUN chmod 555 /task/*
RUN chmod 555 /nsjail.cfg
RUN chmod 555 /run_task.sh
RUN chmod 555 /flag.txt

# For debugging
#RUN apt-get update && \
#    apt-get install -y gdb python git python-pip && \
#    pip install pwntools && \
#    git clone https://github.com/pwndbg/pwndbg /pwndbg && \
#    cd /pwndbg && ./setup.sh

CMD /run_task.sh
