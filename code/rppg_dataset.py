import os
import base64
import numpy as np

PATH = './data/'

class DataReader():
    def __init__(self, path, data) -> None:
        self.path = path
        self.data = data

    def read(self):
        for root, dirs, files in os.walk(self.path):    
            for name in files:
                print(os.path.join(root, name))
    
    def convert_base64(self):
        return base64.b64decode(self.data)

    def iterate(self):
        # for d in self.data:
        #     print(d)
        return None

