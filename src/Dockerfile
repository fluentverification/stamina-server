from debian:latest

ENV API_HOME=/opt/api

RUN apt-get update && apt-get install -y python3 python3-flask python3-docker
RUN mkdir -p $API_HOME

COPY . $API_HOME
WORKDIR $API_HOME/src
ENV FLASK_APP=$API_HOME/src/app.py
RUN env FLASK_APP=$FLASK_APP flask run 
