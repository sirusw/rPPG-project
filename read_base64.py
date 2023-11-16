import base64
import cv2
import numpy as np
# File Path to Read Base64 Frames
file_path = "data/data1.txt"

def read_base64_file(file_path):
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

# Read Base64 Frames from File
frames = read_base64_file(file_path)

# Display Frames
for frame in frames:
    cv2.imshow('Frame', frame)
    cv2.waitKey(1)

cv2.destroyAllWindows()