FROM python:3.7.6-buster

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE app.settings

RUN pip install pandas==1.0.0
RUN pip install numpy

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

