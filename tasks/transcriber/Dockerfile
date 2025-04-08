
# Stage 1: Build the requirements
FROM public.ecr.aws/docker/library/python:3.12.3-slim as requirements-stage

WORKDIR /tmp

ENV POETRY_VERSION=1.8.2

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml /tmp/
RUN curl -sSL https://install.python-poetry.org | python - --version ${POETRY_VERSION} && \
    export PATH="/root/.local/bin:$PATH" && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2: Build the final image support GPU.    
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04 as base

WORKDIR /app

# Install Python 3.12
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update &&\
    apt install -y software-properties-common wget && \
    add-apt-repository ppa:deadsnakes/ppa &&\
    apt-get -y install --no-install-recommends default-mysql-client && \
    apt update &&\
    apt install -y python3.12 &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Pip
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.12 get-pip.py && \
    rm get-pip.py

# Configure Python 3.12 as the default python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 &&\
    update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

# Install Libs
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt --break-system-packages

COPY src /app/src

ENV PYTHONPATH=/app

