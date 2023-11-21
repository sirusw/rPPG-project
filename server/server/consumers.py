# myapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logging.info("New WebSocket connection")
        await self.channel_layer.group_add(
            'video',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        logging.info("WebSocket connection closed")
        await self.channel_layer.group_discard(
            'video',
            self.channel_name
        )

    async def video_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "video.update",
            'frame': event['frame'], 
        }))
        return