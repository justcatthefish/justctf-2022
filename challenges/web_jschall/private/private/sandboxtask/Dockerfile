# build app
FROM golang:1.18.3-stretch as builder_app
WORKDIR /code/
COPY backend .
RUN go build -v ./cmd/main/

# build nginx module
FROM ubuntu:22.04 as builder_nginx

WORKDIR /tmp/
RUN apt-get update -y
RUN apt-get install -y nginx
RUN apt-get install -y wget curl git gcc
RUN apt install -y libperl-dev libgeoip-dev libgd-dev libxslt1-dev libpcre3-dev libssl-dev
RUN apt-get install -y make

RUN NGINX_VERSION=$(nginx -v 2>&1 | awk -F 'nginx/' '{ print $2 }' | awk '{ print $1 }') && \
    wget https://nginx.org/download/nginx-$NGINX_VERSION.tar.gz && \
    tar -xzf nginx-$NGINX_VERSION.tar.gz && \
    export NGINX_PATH=$(pwd)/nginx-$NGINX_VERSION/ && \
    git clone https://github.com/simon987/ngx_http_js_challenge_module && \
    cd ngx_http_js_challenge_module && \
    ./build.sh && \
    cp /tmp/nginx-$NGINX_VERSION/objs/ngx_http_js_challenge_module.so /tmp/ngx_http_js_challenge_module.so

# build all
FROM ubuntu:22.04
RUN apt-get update -y && apt-get install -y wget curl unzip gnupg

# install nginx
RUN apt-get install -y nginx

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -  && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get -y update && \
    apt-get install -y google-chrome-stable

# install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
        unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install iptables
RUN apt-get install -y iptables

RUN groupadd -g 99999 justctf && \
    useradd --uid 99999 --gid 99999 justctf && \
    mkdir /home/justctf && \
    chown justctf /home/justctf -R && \
    chmod 755 /home/justctf -R

WORKDIR /home/justctf/
USER justctf
COPY --from=builder_app /code/main app

# nginx files
USER root
COPY --from=builder_nginx /tmp/ngx_http_js_challenge_module.so /usr/lib/nginx/modules/
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/loader.html /etc/nginx/loader.html
COPY public /public/

RUN mkdir -p /nginx/proxy && \
    mkdir -p /nginx/cache && \
    mkdir -p /nginx/body && \
    mkdir -p /nginx/fastcgi && \
    mkdir -p /nginx/uwsgi && \
    mkdir -p /nginx/scgi && \
    chown www-data /nginx/ -R && \
    chmod 755 /nginx/ -R

# scripts
USER root
COPY scripts /scripts
RUN chmod +x /scripts/iptables.sh && \
    chmod +x /scripts/run.sh
CMD ["/scripts/run.sh"]
