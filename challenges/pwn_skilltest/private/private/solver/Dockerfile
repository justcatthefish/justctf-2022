FROM disconnect3d/pwntools:ubuntu22.04-pwntools
RUN mkdir -p /solver
COPY skilltest solve.py libc-2.34.so /solver/
RUN chmod 777 /solver/*
WORKDIR /solver

