# syntax=docker/dockerfile:1
FROM python:3.10-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install -y socat

COPY . .

EXPOSE 4444
EXPOSE 4445
CMD "./serve_all.sh"
