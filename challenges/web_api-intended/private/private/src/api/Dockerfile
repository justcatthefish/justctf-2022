FROM tiangolo/uvicorn-gunicorn:python3.9

WORKDIR /python

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN groupadd -g 99999 jailed && \
    useradd --uid 99999 --gid 99999 jailed && \
    mkdir /home/jailed && \
    chown jailed /home/jailed -R && \
    chmod 755 /home/jailed -R && \
    chown jailed:jailed /python -R
USER jailed

CMD [ "uvicorn", "main:app" , "--host=0.0.0.0", "--port=8181"]
