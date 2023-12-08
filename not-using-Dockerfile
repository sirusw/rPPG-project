# Stage 1: Build the React frontend
FROM node:18 AS frontend
WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend/ ./
RUN npm run build

# Stage 2: Run the MQTT broker
FROM eclipse-mosquitto AS mqtt
COPY ./mosquitto/mosquitto.conf /mosquitto/config/mosquitto.conf

# Stage 3: Run the Redis server
FROM redis:latest AS redis
CMD [ "redis-server" ]

# Stage 4: Run the Django backend
FROM python:3.10 AS backend
WORKDIR /app
COPY ./server/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./server/ ./
CMD ["python", "manage.py", "mqttclient"]
CMD ["daphne", "server.asgi:application"]

# Stage 5: Run the Python script
FROM python:3.10 AS script
WORKDIR /app
RUN apt-get update && apt-get install -y cmake
COPY ./code/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./code/main.py ./
CMD ["python", "main.py"]

# Final stage: Combine all services
FROM ubuntu:latest
COPY --from=frontend /app/build /app/frontend
COPY --from=mqtt /mosquitto /app/mosquitto
COPY --from=redis /data /data
COPY --from=backend /app /app/server
COPY --from=script /app/main.py /app/code/main.py
