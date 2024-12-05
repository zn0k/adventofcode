FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

RUN apt update

RUN pip install --upgrade pip

COPY .devcontainer/requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt