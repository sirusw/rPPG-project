import os
import base64
import numpy as np
import cv2

from utils import read_base64

class DataReader():
    def __init__(self, path, data) -> None:
        self.path = path
        self.data = data

    def read(self):
        file_list = []
        for root, dirs, files in os.walk(self.path):    
            for name in files:
                file_list.append(os.path.join(root, name))
        for file in file_list:
            file_data = read_base64(file)
            self.data.append(file_data)
        return self.data
    

    def iterate(self):
        # for d in self.data:
        #     print(d)
        return None

