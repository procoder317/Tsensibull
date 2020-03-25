FROM python:3.6.5

MAINTAINER kanaha001@gmail.com

ENV PYTHONUNBUFFERED 1
WORKDIR /tsproj
COPY ./tsproj/requirements.txt /tsproj/requirements.txt
RUN pip install -r requirements.txt
ADD ./tsproj /tsproj