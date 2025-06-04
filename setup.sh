#!/bin/bash

mkdir mosquitto/data
mkdir mosquitto/log

python -m venv .venv

source .venv/bin/activate
pip install --upgrade pip
pip install paho-mqtt PyQt5 influxdb
