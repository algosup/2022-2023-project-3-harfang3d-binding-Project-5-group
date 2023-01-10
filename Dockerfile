FROM python:3

LABEL version="1.0"
LABEL customname="FABGen-tests" 

WORKDIR /usr/src/tests

COPY requirements.txt /usr/src/tests
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt update -y && apt upgrade -y

RUN apt-get install -y lua5.4

RUN wget https://go.dev/dl/go1.19.4.linux-amd64.tar.gz
RUN tar -C /usr/local/ -xzf go1.19.4.linux-amd64.tar.gz
RUN export PATH=$PATH:/usr/local/go/bin