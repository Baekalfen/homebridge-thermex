FROM python:3.11-buster

RUN pip install paho-mqtt aiohttp

COPY api.py /api.py
COPY main.py /main.py