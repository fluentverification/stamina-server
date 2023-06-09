# from debian:latest
# 
# ENV API_HOME=/opt/api
# 
# RUN apt-get update && apt-get install -y python3 python3-flask python3-docker
# RUN mkdir -p $API_HOME
# 
# COPY . $API_HOME
# WORKDIR $API_HOME/src
# ENV FLASK_APP=$API_HOME/src/app.py
# RUN env FLASK_APP=$FLASK_APP flask run 
# 
# 
# RUN apk --update add bash
# ENV STATIC_URL /static
# ENV STATIC_PATH /var/www/app/static
# COPY ./requirements.txt /var/www/requirements.txt
# RUN pip install -r /var/www/requirements.txt

# Run with docker run -v /var/run/docker.sock:/var/run/docker.sock

# FROM tiangolo/uwsgi-nginx-flask:latest
FROM debian:latest

ENV API_HOME=/var/www/stamina
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

