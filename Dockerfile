FROM python:3.11-buster

RUN pip install paho-mqtt websocket-client

COPY api.py /api.py
COPY main.py /main.py