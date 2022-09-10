FROM disconnect3d/nsjail:3.1-6483728

RUN groupadd -g 99999 jailed && \
    useradd --uid 99999 --gid 99999 jailed && \
    mkdir /home/jailed && \
    chown jailed /home/jailed -R && \
    chmod 755 /home/jailed -R

RUN mkdir /task

# Copy files
COPY nsjail.cfg /
COPY run_task.sh /

WORKDIR /home
COPY bin/dumpme /task/dumpme
RUN chmod 4111 /task/dumpme

CMD /run_task.sh
