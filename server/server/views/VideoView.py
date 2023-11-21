from django.http import JsonResponse
from models import Video
import paho.mqtt.client as mqtt
import numpy as np
import cv2
import base64
from django.core.files import File
from datetime import datetime
import os

# Global variables
client = mqtt.Client()
client.username_pw_set("mqtt", 1234)  # Replace with your MQTT username and password
broker = "52.15.88.211"
port = 18839 # Replace with your MQTT broker's port
topic = "/data/tx"
recording = False
frames = []

def mqtt_setup():
    global client, broker, port
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)  # Connect to the MQTT broker
    client.loop_start()  # Start the client loop

mqtt_setup()

# MQTT event handlers
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)  # Replace with your MQTT topic

def on_message(client, userdata, msg):
    global recording, frames

    if recording:
        # Convert the base64 string back to a numpy array
        img_array = np.frombuffer(base64.b64decode(msg.payload), dtype=np.uint8)
        frame = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
        frames.append(frame)

# Django views
def start_recording(request):
    global recording, frames

    if not recording:
        frames = []  # Reset the frames
        recording = True
        # client.loop_start()
        return JsonResponse({'status': 'Recording started'})

    else:
        return JsonResponse({'status': 'Recording already in progress'})

def stop_recording(request):
    global recording

    if recording:
        recording = False
        # client.loop_stop()

        # Convert frames into video file and save it
        video_file = convert_frames_to_video(frames)

        now = datetime.now()
        video_name = 'video_{}.mp4'.format(now.strftime('%Y%m%d_%H%M%S'))

        # Create a new Video object and save it
        video = Video()
        with open(video_file, 'rb') as f:
            video.video_file.save(video_name, File(f), save=True)

        os.remove(video_file)
        return JsonResponse({'status': 'Recording stopped'})

    else:
        return JsonResponse({'status': 'No recording in progress'})
    

def convert_frames_to_video(frames):
    # Get the shape of the first frame
    height, width, channels = frames[0].shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))

    # Write out all the frames
    for frame in frames:
        out.write(frame)  # Write out frame to video

    # Release everything if job is finished
    out.release()
    return 'output.mp4'