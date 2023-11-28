# myapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
import base64
from django.core.cache import cache

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logging.info("New WebSocket connection: {self.channel_name}")
        await self.channel_layer.group_add(
            'video',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        logging.info("WebSocket connection closed: {self.channel_name}")
        await self.channel_layer.group_discard(
            'video',
            self.channel_name
        )
        cache.delete('video')

    async def video_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "video.update",
            'frame': event['frame'], 
        }))
        return
    
    async def receive(self, text_data):
        # This method is called when the server receives data from the client
        bytes_data = base64.b64decode(text_data)

        # # You can also send the frame to the group, if necessary
        # await self.channel_layer.group_send(
        #     'video',
        #     {
        #         'type': 'video.update',
        #         'frame': text_data
        #     }
        # )