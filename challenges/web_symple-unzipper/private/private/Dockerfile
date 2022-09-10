FROM python:3.10

RUN mkdir /server && mkdir -p /server/static/etc

COPY . /server/

RUN tar czvf server.tar.gz server && mv server.tar.gz /server/
WORKDIR /server

RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "--port", "80", "--host", "0.0.0.0", "server:app"]
