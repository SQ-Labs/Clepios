FROM ubuntu:20.04

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install python3 python3-pip git wget cmake -y


RUN git clone https://github.com/microsoft/SEAL.git /tmp/SEAL
WORKDIR /tmp/SEAL

RUN cmake -S . -B build && cmake --build build && cmake --install build

RUN pip3 install Pyfhel flask

COPY . /app
WORKDIR /app

ENTRYPOINT flask run --host=0.0.0.0