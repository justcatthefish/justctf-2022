FROM golang:alpine

WORKDIR /app
COPY src .

ARG FLAG="flag{here-should-be-real-flag}"
RUN echo "$FLAG" > ./buckets/secret_file

RUN GOOS=windows GOARCH=amd64 go build server.go
RUN apk add zip
RUN cd /app && zip -r /app.zip .
