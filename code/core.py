import base64
import os
import json
import copy
import threading
import time
from queue import Queue

import cv2 as cv
import dlib
import copy
import matplotlib.pyplot as plt
import numpy as np
from obspy.signal.detrend import polynomial, spline
from scipy import signal
from sklearn.decomposition import PCA

import seaborn as sns
sns.set()

class feature2rppg:
    def __init__(self) -> None:
        self.feature = face2feature()
        self.working = True
    
    def streaming(self):
        self.feature.streaming()

    def polynomialize(self, signal):
        return polynomial(signal, order=2)

    def preprocessing(self, rgb_signal):
        data = np.array(rgb_signal)
        data_r = self.polynomialize(data[:, 0])

class face2feature:
    def __init__(self) -> None:
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("./model/shape_predictor_81_face_landmarks.dat")
        
        self.stream = cv.VideoCapture(0)
        self.fps = 24
        self.QUEUE_MAX = 256
        self.QUEUE_WINDOWS = 64
        self.Queue_rawframe = Queue(maxsize=3)

        self.Queue_Sig_left = Queue(maxsize=self.QUEUE_MAX)
        self.Queue_Sig_right = Queue(maxsize=self.QUEUE_MAX)
        self.Queue_Sig_fore = Queue(maxsize=self.QUEUE_MAX)
        self.Queue_Time = Queue(maxsize=self.QUEUE_WINDOWS)

        self.working, self.flag_face, self.flag_queue = False, False, False
        self.sig_left, self.sig_right, self.fore = None, None, None

    def capture_process(self):
        while self.working:
            ret, frame = self.stream.read()
            if ret:
                self.Queue_rawframe.put(frame)
            else:
                print("Error: Capture Process")
                break

    def streaming(self):
        self.working = True
        self.capture_process_ = threading.Thread(target=self.capture)