FROM python:3.11.9-alpine3.20

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt