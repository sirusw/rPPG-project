import base64
import cv2
import numpy as np
import scipy.signal
from PIL import Image
import paho.mqtt.client as mqtt

# MQTT Broker Details
broker = "192.168.0.106"
port = 18839
username = "mqtt"
password = "1234"

# Image Storage Path
image_path = "/path/to/save/image.jpg"

buffer_size = 128  # buffer size for the sliding window of frames
buffer = np.zeros(buffer_size)  # buffer for storing pixel intensity values

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("/data/tx")

def on_message(client, userdata, msg):
    global buffer
    print("Message received!")

    # Decode Base64 Image
    imgdata = base64.b64decode(msg.payload)

    # Convert Bytes to Numpy Array
    nparr = np.frombuffer(imgdata, np.uint8)

    # Convert Numpy Array to Image
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Extract the green channel
    green = img_np[:, :, 1]

    # Calculate the average intensity in the green channel
    intensity = np.mean(green)

    # Add the intensity value to the buffer
    buffer = np.roll(buffer, -1)
    buffer[-1] = intensity

    # Apply a bandpass filter to the intensity values in the buffer to extract
    # the heart rate frequency
    freqs, psd = scipy.signal.welch(buffer, fs=30, nperseg=buffer_size, noverlap=0, window='hamming', scaling='spectrum')
    freq_res = freqs[1] - freqs[0]  # calculate frequency resolution
    heart_rate_freq = freqs[np.argmax(psd[(freqs >= 0.67) & (freqs <= 4.0)])]  # find the peak in the range of human heart rate 
    heart_rate = heart_rate_freq * 60  # convert from Hz to bpm

    # Display the heart rate on the image
    cv2.putText(img_np, f"HR: {heart_rate:.2f} bpm", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Display Image
    cv2.imshow('Received Image', img_np)
    cv2.waitKey(1)  # waits 1 ms and then proceed to next frame

    # Save Image
    # cv2.imwrite(image_path, img_np)

client = mqtt.Client()
client.username_pw_set(username, password)

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)

client.loop_forever()