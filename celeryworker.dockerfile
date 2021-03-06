FROM python:3.8-slim-buster

WORKDIR /worker/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

RUN pip install --upgrade pip

COPY requirements.txt /worker/

RUN pip install -r /worker/requirements.txt

COPY . /worker
