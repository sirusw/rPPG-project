import base64
import cv2
import numpy as np
import scipy.signal
from PIL import Image
import paho.mqtt.client as mqtt
import time
import os

# MQTT Broker Details
broker = "192.168.0.106"
port = 18839
username = "mqtt"
password = "1234"

# Image Storage Path
file_path = "data/data.txt"
record_length = 10  # Length of the recording in seconds

buffer_size = 128  # buffer size for the sliding window of frames
buffer = np.zeros(buffer_size)  # buffer for storing pixel intensity values

# Frame rate calculation variables
frame_count = 0
start_time = None

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("/data/tx")

def on_message(client, userdata, msg):
    global buffer, frame_count, start_time
    print("Message received!")

    # Decode Base64 Image
    imgdata = base64.b64decode(msg.payload)

    # Convert Bytes to Numpy Array
    nparr = np.frombuffer(imgdata, np.uint8)

    # Convert Numpy Array to Image
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Frame rate calculation
    if start_time is None:
        start_time = time.time()
    else:
        end_time = time.time()
        elapsed_time = end_time - start_time
        frame_rate = frame_count / elapsed_time
        start_time = end_time

        # Append frame rate to the data file
        with open(file_path, 'a') as file:
            file.write(f"{frame_rate:.2f} Hz\n")

    # Display Image
    cv2.imshow('Received Image', img_np)
    cv2.waitKey(1)  # waits 1 ms and then proceed to next frame

    with open(file_path, 'a') as file:
        file.write(base64.b64encode(imgdata).decode() + '\n')

    # Check if recording length is reached
    if elapsed_time >= record_length:
        # Disconnect from MQTT broker
        client.disconnect()

try:
    client = mqtt.Client()
    client.username_pw_set(username, password)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)

    start_time = time.time()
    client.loop_start()

    # Wait for the recording to complete
    time.sleep(record_length)

    client.loop_stop()
    cv2.destroyAllWindows()

except KeyboardInterrupt:
    # Rename the data file to include the frame rate and recording length
    frame_rate = frame_count / record_length
    new_file_path = file_path.replace(".txt", f"_{frame_rate:.2f}Hz_{record_length}second.txt")
    os.rename(file_path, new_file_path)