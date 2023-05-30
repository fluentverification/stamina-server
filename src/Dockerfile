from debian:latest

ENV API_HOME=/opt/api
ENV FLASK_APP=app.py

RUN apt-get update && apt-get install -y python3 python3-flask python3-docker
RUN mkdir -p $API_HOME

COPY ./src $API_HOME
WORKDIR $API_HOME
RUN flask run
