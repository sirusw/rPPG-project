# myapp/mqtt.py
import base64
import cv2
import numpy as np
import paho.mqtt.client as mqtt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import time
import random
import asyncio
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor

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
        self.client.loop_start()
        self.received_param = {}
        self.frame_buffer = []
        self.frame_buffer_size = 30
        self.lock = Lock()
        self.executor = ThreadPoolExecutor(max_workers=5)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code "+str(rc))
        client.subscribe("/data/tx")
        client.subscribe("/config/tx")

    def on_message(self, client, userdata, msg):
        if msg.topic == "/config/tx":
            try:
                self.received_param = json.loads(msg.payload.decode())
                print(self.received_param)
            except json.JSONDecodeError:
                print(f"Invalid JSON: {msg.payload.decode()}")
            
            return
        
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
