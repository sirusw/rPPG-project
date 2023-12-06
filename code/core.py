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

from utils import RGB_hist, Hist2Feature
from options import get_options
kwargs = get_options()

import seaborn as sns
sns.set()


class feature2rppg:
    def __init__(self) -> None:
        self.working = True
        self.feature = face2feature()
    
    def streaming(self):
        self.feature.streaming()

    def polynomialize(self, signal):
        return polynomial(signal, order=2)

    def preprocessing(self, rgb_signal):
        data = np.array(rgb_signal)
        data_r = self.polynomialize(data[:, 0])
        data_g = self.polynomialize(data[:, 1])
        data_b = self.polynomialize(data[:, 2])
        return np.array([data_r, data_g, data_b]).T
    
    def Pbv(self, signal):
        signal_mean = np.mean(signal, axis=1)
        signal_norm_r = signal[:, 0] / signal_mean[0]
        signal_norm_g = signal[:, 1] / signal_mean[1]
        signal_norm_b = signal[:, 2] / signal_mean[2]

        pbv_numerator = np.array(
            [np.std(signal_norm_r), np.std(signal_norm_g), np.std(signal_norm_b)])
        pbv_denumerator = np.sqrt(
            np.var(signal_norm_r) + np.var(signal_norm_g) + np.var(signal_norm_b))
        pbv = pbv_numerator / pbv_denumerator

        C = np.array([signal_norm_r, signal_norm_g, signal_norm_b])
        Ct = C.T
        Q = np.matmul(Ct, C)
        W = np.linalg.solve(Q, pbv)
        A = np.matmul(C, Ct)
        B = np.matmul(pbv.T, W)

        return A/B

    def Chrom(self, signal):
        X = signal.copy()
        X_comp = 3 * X[:, 0] - 2 * X[:, 1]
        Y_comp = 1.5 * X[:, 0] + X[:, 1] - 1.5 * X[:, 2]
        sX, sY = np.std(X_comp), np.std(Y_comp)
        alpha = sX / sY

        return X_comp - alpha * Y_comp
    
    def Green_red(self, signal):
        return signal[:, 1] - signal[:, 0]
    
    def Green(self, signal):
        return signal[:, 1]
    
    def transfer2bpm(self, raw_bpm, spec, fps):
        return 0.95 * raw_bpm + 0.05 * np.argmax(spec[:int(len(spec)/2)]) * fps * 60
    
    def __del__(self):
        self.working = False
        self.feature.__del__()

class face2feature:
    def __init__(self) -> None:
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(r"/Users/zihan/Documents/hku/aiot/group proj/rPPG-project/model/shape_predictor_81_face_landmarks.dat")
        
        self.stream = cv.VideoCapture(0)
        # self.stream = cv.VideoCapture("./video.avi")
        # print(f"Total frame: {self.stream.get(cv.CAP_PROP_FRAME_COUNT)}")
        
        if not self.stream.isOpened():
            self.stream.release()
            raise IOError("No input stream")

        self.fps = self.stream.get(cv.CAP_PROP_FPS)
        self.QUEUE_MAX = 256
        self.QUEUE_WINDOWS = 32
        self.Queue_rawframe = Queue(maxsize=3)

        self.Queue_signal_l = Queue(maxsize=self.QUEUE_MAX)
        self.Queue_signal_r = Queue(maxsize=self.QUEUE_MAX)
        self.Queue_signal_f = Queue(maxsize=self.QUEUE_MAX)
        self.Queue_Time = Queue(maxsize=self.QUEUE_WINDOWS)

        self.working, self.flag_face, self.flag_queue = False, False, False
        self.signal_l, self.signal_r, self.signal_f = None, None, None

        self.face_mask = None
        self.frame_display = None

    def streaming(self):
        self.working = True
        self.capture_process_ = threading.Thread(target=self.capture_process)
        self.roi_process_ = threading.Thread(target=self.roi_process)

        self.capture_process_.start()
        self.roi_process_.start()

    def capture_process(self):
        while self.working:
            self.status, frame = self.stream.read()
            self.frame_display = copy.copy(frame)

            if self.Queue_Time.full():
                self.Queue_Time.get_nowait()
                # self.fps = 1 / \
                #     np.mean(np.diff(np.array(list(self.Queue_Time.queue))))
            
            if not self.status:
                self.working = False
                break

            if self.Queue_rawframe.full():
                self.Queue_rawframe.get_nowait()
            else:
                self.Queue_Time.put_nowait(time.time())
            
            try:
                self.Queue_rawframe.put_nowait(frame)
            except Exception as e:
                pass
    
    def roi_process(self):
        print('roi_process activated......')
        while self.working:
            try: 
                frame = self.Queue_rawframe.get_nowait()
            except Exception as e:
                continue

            roi_l, roi_r, roi_f = self.roi(frame)
            
            if roi_l is not None and roi_r is not None and roi_f is not None:
                self.hist_l = RGB_hist(roi_l)
                self.hist_r = RGB_hist(roi_r)
                self.hist_f = RGB_hist(roi_f)
                print(self.Queue_signal_l.qsize(), self.Queue_signal_r.qsize(), self.Queue_signal_f.qsize())
                print(self.flag_queue)
                if self.Queue_signal_l.full():
                    self.signal_l = copy.copy(list(self.Queue_signal_l.queue))
                    self.Queue_signal_l.get_nowait()
                    self.flag_queue = True
                else:
                    self.flag_queue = False

                if self.Queue_signal_r.full():
                    self.signal_r = copy.copy(list(self.Queue_signal_r.queue))
                    self.Queue_signal_r.get_nowait()
                    self.flag_queue = True
                else:
                    self.flag_queue = False
                
                if self.Queue_signal_f.full():
                    self.signal_f = copy.copy(list(self.Queue_signal_f.queue))
                    self.Queue_signal_f.get_nowait()
                    self.flag_queue = True
                else:
                    self.flag_queue = False

                self.Queue_signal_l.put_nowait(Hist2Feature(self.hist_l))
                self.Queue_signal_r.put_nowait(Hist2Feature(self.hist_r))
                self.Queue_signal_f.put_nowait(Hist2Feature(self.hist_f))
            
            else:
                print('Data is cleared')
                self.hist_l, self.hist_r, self.hist_f = None, None, None
                self.Queue_signal_l.queue.clear()
                self.Queue_signal_r.queue.clear()
                self.Queue_signal_f.queue.clear()


    def marker(self, frame):
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = self.detector(frame_gray)
        if len(faces) == 1:
            face = faces[0]
            landmarks = [[p.x, p.y] for p in self.predictor(frame_gray, face).parts()]
        try:
            return landmarks
        except:
            return None

    def roi(self, frame):
        frame = cv.GaussianBlur(frame, (5, 5), 0)
        landmark = self.marker(frame)

        cheek_l = [1, 2, 3, 4, 48, 31, 28, 39]
        cheek_r = [15, 14, 14, 12, 54, 35, 28, 42]
        forehead = [69, 70, 71, 80, 72, 25, 24, 23, 22, 21, 20, 19, 18]

        mask_l = np.zeros(frame.shape, dtype=np.uint8)
        mask_r = np.zeros(frame.shape, dtype=np.uint8)
        mask_f = np.zeros(frame.shape, dtype=np.uint8)
        mask_display = np.zeros(frame.shape, dtype=np.uint8)

        try:
            self.flag_face = True
            pts_l = np.array(
                [landmark[i] for i in cheek_l], np.int32).reshape((-1, 1, 2))
            pts_r = np.array(
                [landmark[i] for i in cheek_r], np.int32).reshape((-1, 1, 2))
            pts_f = np.array(
                [landmark[i] for i in forehead], np.int32).reshape((-1, 1, 2))
            
            mask_l = cv.fillPoly(mask_l, [pts_l], (255, 255, 255))
            mask_r = cv.fillPoly(mask_r, [pts_r], (255, 255, 255))
            mask_f = cv.fillPoly(mask_f, [pts_f], (255, 255, 255))
        
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (15, 30))
            mask_l = cv.erode(mask_l, kernel, iterations=1)
            mask_r = cv.erode(mask_r, kernel, iterations=1)
            mask_f = cv.erode(mask_f, kernel, iterations=1)

            mask_display_l, mask_display_r, mask_display_f = copy.copy(mask_l), copy.copy(mask_r), copy.copy(mask_f)
            mask_display_l[:, :, 1] = 0
            mask_display_r[:, :, 0] = 0
            mask_display_f[:, :, 2] = 0

            mask_display = cv.bitwise_or(mask_display_l, mask_display_r)
            mask_display = cv.bitwise_or(mask_display, mask_display_f)
            self.face_mask = cv.addWeighted(mask_display, 0.25, frame, 1, 0)

            roi_l = cv.bitwise_and(mask_l, frame)
            roi_r = cv.bitwise_and(mask_r, frame)
            roi_f = cv.bitwise_and(mask_f, frame)

            return roi_l, roi_r, roi_f
        
        except Exception as e:
            self.face_mask = frame
            self.flag_face = False
            return None, None, None
            

    def __del__(self):
        self.working = False
        self.stream.release()
        cv.destroyAllWindows()

if __name__ == '__main__':
    f2f = face2feature()
    f2f.streaming()
    while True:
        time.sleep(1)
        print(f2f.fps)
