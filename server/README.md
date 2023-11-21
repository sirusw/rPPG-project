# Server backend
This is the backend Django application for receiving MQTT messages, perform face detection and rPPG algorithms, then streaming to the front-end.

## Setup Instructions

1. Install the dependencies.

```bash
pip install -r requirements.txt
```

2. **Set up Redis** at 127.0.0.1:6379. You'll need to install WSL, then download Redis and run it.

```bash
sudo service redis-server start
```

```bash
sudo service redis-server status
```

3. Start the Daphne server.

```bash
daphne server.asgi:application
```

This will start the Daphne ASGI server, which serves the Django application and handles WebSocket connections. It takes input from the MQTT client, and handles connection from front-end.

4. In a new terminal window, start the MQTT client.

```bash
python manage.py mqttclient
```

This will start the MQTT client, which listens for MQTT messages and forwards them to the WebSocket.
