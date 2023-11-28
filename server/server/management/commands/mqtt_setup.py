# myapp/mqtt.py
import base64
import cv2
import numpy as np
import paho.mqtt.client as mqtt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# client = None



# def on_connect(client, userdata, flags, rc):
#     print("Connected to MQTT broker with result code "+str(rc))
#     client.subscribe("/data/tx")

# def on_message(client, userdata, msg):
#     # Decode base64 data to get video frame
#     # decoded_data = base64.b64decode(msg.payload)
#     # np_data = np.frombuffer(decoded_data, np.uint8)
#     # frame = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

#     frame_base64 = msg.payload.decode('utf-8')

#     # # Convert to grayscale
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # # Detect faces
#     # faces = face_cascade.detectMultiScale(gray, 1.1, 4)

#     # # If at least one face is detected, draw rectangle around the first one
#     # if len(faces) > 0:
#     #     (x, y, w, h) = faces[0]
#     #     # Draw rectangle around the face
#     #     cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

#     # Re-encode the frame to base64 so it can be sent to the frontend
#     # retval, buffer = cv2.imencode('.jpg', frame)
#     # frame_base64 = base64.b64encode(buffer).decode('utf-8')

#     channel_layer = get_channel_layer()

#     # Send results to frontend
#     async_to_sync(channel_layer.group_send)(
#         "video",
#         {
#             "type": "video.update",
#             "frame": frame_base64,
#         }
#     )


# def start_mqtt_client():
#     global client
#     client = mqtt.Client(transport="websockets")

#     # Set username and password for mqtt client
#     client.username_pw_set("mqtt", "1234")

#     client.on_connect = on_connect
#     client.on_message = on_message

#     client.connect("127.0.0.1", 9001)

#     client.loop_start()

# start_mqtt_client()

class MQTTClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.client = mqtt.Client(transport="websockets")
        self.client.username_pw_set("mqtt", "1234")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("127.0.0.1", 9001)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code "+str(rc))
        client.subscribe("/data/tx")

    def on_message(self, client, userdata, msg):
        frame_base64 = msg.payload.decode('utf-8')

        channel_layer = get_channel_layer()

        # Send results to frontend
        async_to_sync(channel_layer.group_send)(
            "video",
            {
                "type": "video.update",
                "frame": frame_base64,
            }
        )
    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("MQTT client stopped")

# Return the single instance of MQTTClient
mqtt_client = MQTTClient.get_instance()
