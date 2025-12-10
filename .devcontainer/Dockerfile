FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

RUN apt update

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

RUN uv venv /opt/venv

ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:${PATH}"

COPY .devcontainer/requirements.txt /tmp/requirements.txt

RUN uv pip install -r /tmp/requirements.txt
