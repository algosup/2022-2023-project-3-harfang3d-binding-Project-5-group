FROM python:3

LABEL version="1.0"
LABEL customname="FABGen-tests" 

WORKDIR /usr/src/tests

COPY requirements.txt /usr/src/tests
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt update -y && apt upgrade -y

RUN apt-get install -y rustc

RUN apt-get install -y lua5.4

RUN apt-get install -y golang

RUN apt-get install -y xdg-utils --fix-missing

RUN apt-get install -y cmake