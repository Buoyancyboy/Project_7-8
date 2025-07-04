FROM node

# Stel de werkdirectory in
WORKDIR /app

COPY ./src/hmi_frontend/ /app

# Installeer de benodigde npm-modules
RUN npm install

EXPOSE 3000

# Start de applicatie
CMD ["npm", "start"]