# Run on debian
FROM debian:latest

# Serve from /var/www
ENV API_HOME=/var/www/stamina
# In order to serve over HTTPS, you will need an OpenSSL certificate
# This file assumes taht you have certificate files httpcert.crt and httpkey.key
ENV CRT_FILE=httpcert.crt
ENV KEY_FILE=httpkey.key
ENV PORT=8443

RUN mkdir -p $API_HOME
COPY . $API_HOME
WORKDIR $API_HOME

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y libssl-dev
RUN apt-get install -y python3 python3-pip python3-venv
RUN python3 -m pip install flask docker build uwsgi

RUN python3 -m build
RUN python3 -m pip install .

RUN uwsgi --master --https 0.0.0.0:$PORT,$CRT_FILE,$KEY_FILE -p 4 -w stamina_API:app

