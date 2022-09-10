# syntax=docker/dockerfile:1
FROM python:3.10-bullseye

RUN pip install --no-cache-dir fastecdsa==2.2.3

RUN apt update && apt install -y hashcash && rm -rf /var/lib/apt/lists/*

COPY . /
