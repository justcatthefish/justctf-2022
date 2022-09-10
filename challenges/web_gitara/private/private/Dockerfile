FROM php:8.1-apache

RUN apt-get update && apt-get install -y git sshpass && rm -rf /var/lib/apt/lists/*

COPY index.php /var/www/html/
