# syntax=docker/dockerfile:1
FROM python:3.10-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt  

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

COPY ./src ./src
COPY ./serve.sh ./

RUN groupadd -g 99999 jailed && \
    useradd --uid 99999 --gid 99999 jailed && \
    mkdir /home/jailed && \
    chown jailed /home/jailed -R && \
    chmod 755 /home/jailed -R

USER 99999

CMD "./serve.sh"
