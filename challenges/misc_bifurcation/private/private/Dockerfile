FROM python:3.10

RUN groupadd -g 99999 jailed && \
    useradd --uid 99999 --gid 99999 jailed && \
    mkdir /home/jailed && \
    chown jailed /home/jailed -R && \
    chmod 755 /home/jailed -R

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN mkdir /task

# Copy files
COPY run_task.sh /

WORKDIR /home
COPY game.py /task/game.py
COPY tree.py /task/tree.py
RUN chmod 755 /task/game.py

USER jailed

CMD /run_task.sh
