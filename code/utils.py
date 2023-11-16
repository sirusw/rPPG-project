import base64
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

import options
kwargs = options.get_options()

def plot_data(x, y, title, xlabel, ylabel):
    plt.figure()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def read_base64(file_path):
    frames = []
    with open(file_path, 'r') as file:
        for line in file:
            # Remove new line symbol
            line = line.strip()
            # Decode Base64 frame
            frame_data = base64.b64decode(line)
            # Convert Bytes to Numpy Array
            nparr = np.frombuffer(frame_data, np.uint8)
            # Convert Numpy Array to Image
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # Append frame to the list
            frames.append(frame)
    return frames

def save(data, file: str):
    if not os.path.exists(kwargs["save_path"]):
        os.mkdir(kwargs["save_path"])
    file_path = kwargs["save_path"] + file
    np.save(file_path, data)
    return file_path

if __name__ == "__main__":
    text = b'binary\x00string'
    output = base64.b64encode(text)
    print(output)
