FROM php:8-cli

RUN set -e; apt-get update; \
    apt-get install -y --no-install-recommends libffi-dev; \
    apt-get remove -y curl; \
    docker-php-ext-configure ffi; \
    docker-php-ext-install -j$(nproc) ffi pcntl;

RUN groupadd ctf
RUN useradd -G ctf --home=/pwn pwn

WORKDIR /app
COPY index.php /app
COPY itsgone.gif /app
COPY php.ini /usr/local/etc/php/conf.d/docker-php-ext-ffi.ini

USER pwn
CMD [ "php","-S","0.0.0.0:5000" ]