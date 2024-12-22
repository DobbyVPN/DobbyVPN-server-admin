# FROM python:3.10-slim
FROM alpine:latest

RUN apk add --no-cache \
    python3 \
    py3-pip \
    git

WORKDIR /app

RUN git clone https://github.com/DobbyVPN/DobbyVPN-server-admin.git
RUN mv /app/DobbyVPN-server-admin/* /app/ && rm -rf /app/DobbyVPN-server-admin

RUN python3 -m venv /app/venv && \
    . /app/venv/bin/activate && \
    pip install --no-cache-dir -r /app/requirements.txt



CMD ["/app/venv/bin/python", "/app/main.py"]
