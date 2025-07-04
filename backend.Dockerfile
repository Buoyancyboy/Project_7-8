FROM python:3.9-slim

# Stel de werkdirectory in
WORKDIR /app

COPY ./src/ /app/

# Installeer de benodigde Python-pakketten
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# Start de applicatie
CMD ["python", "manage.py", "runserver"]