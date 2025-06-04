FROM python:3.9-slim

# Stel de werkdirectory in
WORKDIR /app

# Kopieer de projectbestanden naar de container
COPY ./src /app

# Installeer de benodigde Python-pakketten
RUN pip install --upgrade pip
RUN pip install paho-mqtt PyQt5 influxdb

# Start de applicatie
CMD ["python", "main.py"]