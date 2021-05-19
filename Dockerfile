FROM python:3.8-slim-buster

WORKDIR /backend/

RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

RUN pip install --upgrade pip

COPY requirements.txt /backend/

RUN pip install -r /backend/requirements.txt
COPY ./app /backend