FROM python:3.7.6-buster

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE app.settings

#RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
#RUN apk add --update --no-cache py3-numpy py3-pandas@testing
#ENV PYTHONPATH=/usr/lib/python3.8/site-packages

RUN pip install pandas==1.0.0
RUN pip install numpy

COPY ./requirements.txt /requirements.txt

#RUN sudo apt add --update --no-cache postgresql-client jpeg-dev
#
#RUN sudo apt --update --no-cache --virtual .tmp-build-deps \
#    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

