# myapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
import base64
from django.core.cache import cache
import asyncio
import subprocess
import redis

def clear_redis_channel():
    # Clear Redis channel messages
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()
    print("Redis channel cleared")

def get_redis_memory_capacity():
    # Get Redis memory and capacity information using WSL command
    redis_info_command = ['wsl', 'redis-cli', 'info', 'memory']
    redis_info_process = subprocess.run(redis_info_command, capture_output=True, text=True)
    return redis_info_process.stdout

class VideoConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = None

    async def connect(self):
        logging.info("New WebSocket connection: {self.channel_name}")
        clear_redis_channel()
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
        clear_redis_channel()

    async def video_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "video.update",
            'frame': event['frame'], 
        }))
        return
    
    async def video_hr(self, event):
        await self.send(text_data=json.dumps({
            "type": "video.hr",
            'hr': event['hr'], 
        }))
        return
    
    async def receive(self, text_data):
        # This method is called when the server receives data from the client
        json_data = json.loads(text_data)
        # if self.timer is not None:
        #     self.timer.cancel()
        bytes_data = base64.b64decode(json_data['frame'])
        

        # self.timer = asyncio.create_task(self.reset_flag())

    

    # async def reset_flag(self):
    #     await asyncio.sleep(3)
    #     self.receiving_from_frontend = False