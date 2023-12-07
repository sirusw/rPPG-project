import threading
import time
import copy
from queue import Queue

import cv2 as cv
import dlib
from obspy.signal.detrend import polynomial
import numpy as np

import matplotlib.pyplot as plt
from utils import Hist2Feature, RGB_hist

import seaborn as sns
sns.set()


class face2feature:
    def __init__(self) -> None:
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('./code/model/shape_predictor_81_face_landmarks.dat')
        self.cam = cv.VideoCapture(0)

        self.fps = 24
        self.QUEUE_MAX = 256
        self.QUEUE_WINDOWS = 64
        self.Queue_rawframe = Queue(maxsize=3)
        self.Queue_Sig_l = Queue(maxsize=self.QUEUE_MAX)
        self.Queue_Sig_r = Queue(maxsize=self.QUEUE_MAX)
        self.Queue_Sig_f = Queue(maxsize=self.QUEUE_MAX)

        self.Queue_Time = Queue(maxsize=self.QUEUE_WINDOWS)

        self.working = False
        self.flag_face = False
        self.flag_Queue = False

        self.frame_display = None
        self.face_mask = None

        self.Sig_l = None
        self.Sig_r = None
        self.Sig_f = None

    # Initialize process and start

    def streaming(self):
        self.working = True
        self.capture_process_ = threading.Thread(target=self.capture_process)
        self.roi_process_ = threading.Thread(target=self.roi_process)
        self.capture_process_.start()
        self.roi_process_.start()

    # Process: capture frame from camera in specific fps of the camera
    def capture_process(self):
        while self.working:
            self.ret, frame = self.cam.read()
            self.frame_display = copy.copy(frame)
            if self.Queue_Time.full():
                self.Queue_Time.get_nowait()
                self.fps = 1 / np.mean(np.diff(np.array(list(self.Queue_Time.queue))))

            if not self.ret:
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

    # Process: calculate roi from raw frame
    def roi_process(self):
        while self.working:
            try:
                frame = self.Queue_rawframe.get_nowait()
            except Exception as e:
                continue

            roi_l, roi_r, roi_f = self.roi(frame)
            if roi_l is not None and roi_r is not None and roi_f is not None:
                # produce rgb hist of mask (removed black)
                self.hist_l = RGB_hist(roi_l)
                self.hist_r = RGB_hist(roi_r)
                self.hist_f = RGB_hist(roi_f)
                if self.Queue_Sig_l.full():
                    self.Sig_l = copy.copy(list(self.Queue_Sig_l.queue))
                    self.Queue_Sig_l.get_nowait()
                else:
                    self.flag_Queue = False
                if self.Queue_Sig_r.full():
                    self.Sig_r = copy.copy(
                        list(self.Queue_Sig_r.queue))
                    self.Queue_Sig_r.get_nowait()
                else:
                    self.flag_Queue = False
                if self.Queue_Sig_f.full():
                    self.Sig_f = copy.copy(list(self.Queue_Sig_f.queue))
                    self.Queue_Sig_f.get_nowait()
                    self.flag_Queue = True
                else:
                    self.flag_Queue = False

                self.Queue_Sig_l.put_nowait(
                    Hist2Feature(self.hist_l))
                self.Queue_Sig_r.put_nowait(
                    Hist2Feature(self.hist_r))
                self.Queue_Sig_f.put_nowait(
                    Hist2Feature(self.hist_f))

            else:
                self.hist_l, self.hist_r, self.hist_f = None, None, None
                self.Queue_Sig_l.queue.clear()
                self.Queue_Sig_r.queue.clear()
                self.Queue_Sig_f.queue.clear()

    # Get the markpoint of the faces

    def Marker(self, frame):
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = self.detector(frame_gray)
        if len(faces) == 1:
            face = faces[0]
            landmarks = [[p.x, p.y]
                         for p in self.predictor(frame, face).parts()]
        try:
            return landmarks
        except:
            return None


    def roi(self, frame):
        frame = cv.GaussianBlur(frame, (5, 5), 0)
        landmark = self.Marker(frame)

        cheek_l = [1, 2, 3, 4, 48, 31, 28, 39]
        cheek_r = [15, 14, 14, 12, 54, 35, 28, 42]
        forehead = [69, 70, 71, 80, 72, 25, 24, 23, 22, 21, 20, 19, 18]

        mask_l = np.zeros(frame.shape, np.uint8)
        mask_r = np.zeros(frame.shape, np.uint8)
        mask_f = np.zeros(frame.shape, np.uint8)
        mask_display = np.zeros(frame.shape, np.uint8)

        try:
            self.flag_face = True
            pts_l = np.array(
                [landmark[i] for i in cheek_l], np.int32).reshape((-1, 1, 2))
            pts_r = np.array(
                [landmark[i] for i in cheek_r], np.int32).reshape((-1, 1, 2))
            pts_f = np.array([landmark[i]
                                 for i in forehead], np.int32).reshape((-1, 1, 2))
            mask_l = cv.fillPoly(mask_l, [pts_l], (255, 255, 255))
            mask_r = cv.fillPoly(mask_r, [pts_r], (255, 255, 255))
            mask_f = cv.fillPoly(
                mask_f, [pts_f], (255, 255, 255))

            # Erode Kernel: 30
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (15, 30))
            mask_l = cv.erode(mask_l, kernel=kernel, iterations=1)
            mask_r = cv.erode(mask_r, kernel=kernel, iterations=1)
            mask_f = cv.erode(
                mask_f, kernel=kernel, iterations=1)
            # mask = cv.bitwise_or(mask_l, mask_r)
            mask_display_l, mask_display_r = copy.copy(
                mask_l), copy.copy(mask_r)
            mask_display_f = copy.copy(mask_f)

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
        self.cam.release()
        cv.destroyAllWindows()

class feature2rppg():
    def __init__(self) -> None:
        self.series_class = face2feature()
        self.working = True

    def streaming(self):
        self.series_class.streaming()

    def Signal_Preprocessing(self, rgbsig):
        data = np.array(rgbsig)
        data_r = polynomial(data[:, 0], order=2)
        data_g = polynomial(data[:, 1], order=2)
        data_b = polynomial(data[:, 2], order=2)
        return np.array([data_r, data_g, data_b]).T

    def Signal_Preprocessing_single(self, sig):
        return polynomial(sig, order=2)

    def CHROM(self, signal):
        X = signal
        Xcomp = 3*X[:, 0] - 2*X[:, 1]
        Ycomp = (1.5*X[:, 0])+X[:, 1]-(1.5*X[:, 2])
        sX = np.std(Xcomp)
        sY = np.std(Ycomp)
        alpha = sX/sY
        bvp = Xcomp - alpha * Ycomp
        return bvp

    def transfer2bmp(self, beta, _bpm, spec, fps):
        return beta * _bpm + (1 - beta) * np.argmax(spec[:int(len(spec)/2)])/len(spec) * fps * 60

    def __del__(self):
        self.working = False
        self.series_class.__del__()
