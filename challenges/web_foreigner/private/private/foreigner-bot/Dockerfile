# probably better to use curlimages/curl instead
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive 

RUN apt update && apt install curl -yy

RUN mkdir /app
WORKDIR /app
ADD ./run.sh /app/run.sh
RUN chmod +x /app/run.sh
CMD ["/app/run.sh"]