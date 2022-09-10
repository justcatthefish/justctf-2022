FROM disconnect3d/pwntools:ubuntu22.04-pwntools
RUN apt-get update && apt-get install -y --no-install-recommends binutils-aarch64-linux-gnu && rm -rf /var/lib/apt/lists/*
COPY solve.py /solve.py
