FROM python:3.11.7-bookworm

LABEL maintainer="alfmorais"

WORKDIR /code/
COPY requirements.txt /code/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN apt-get update && \
  apt-get install -y --no-install-recommends

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/.
EXPOSE 80

RUN chmod +x wait-for-it.sh
