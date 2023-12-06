import time
import random

from obspy.signal.detrend import spline
from scipy import signal
import numpy as np
import cv2 as cv
import pyqtgraph as pg

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

from core import feature2rppg
from utils import butterworth_filter
import matplotlib.pyplot as plt

MIN_HZ = 0.8
MAX_HZ = 2.5

def butterworth_filter(stream, low, high, sample_rate, order=11):
    nyquist_rate = sample_rate * 0.5
    low /= nyquist_rate
    high /= nyquist_rate
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.lfilter(b, a, stream)

class Main():
    def __init__(self):
        self.processor = feature2rppg()
        self.processor.streaming()
        self.mode = self.processor.Chrom

        self.bpm_f, self.bpm_l, self.bpm_r, self.bpm_avg = 60, 60, 60, 60
        self.conf_f, self.conf_l, self.conf_r = 1, 1, 1

    def DisplayBpm(self):
        signal_f = np.array(self.processor.feature.signal_f)
        signal_l = np.array(self.processor.feature.signal_l)
        signal_r = np.array(self.processor.feature.signal_r)
        # print('size of signal_f: ', signal_f.shape)

        if self.processor.feature.flag_queue:
            self.bvp_f = self.mode(signal_f)
            self.bvp_l = self.mode(signal_l)
            self.bvp_r = self.mode(signal_r)

            self.conf_f = 1 / (max(self.bvp_f) - min(self.bvp_f))
            self.conf_l = 1 / (max(self.bvp_l) - min(self.bvp_l))
            self.conf_r = 1 / (max(self.bvp_r) - min(self.bvp_r))

            self.bvp_f = butterworth_filter(self.processor.polynomialize(self.bvp_f), 
                                            MIN_HZ, MAX_HZ, self.processor.feature.fps, order=5)
            self.bvp_l = butterworth_filter(self.processor.polynomialize(self.bvp_l), 
                                            MIN_HZ, MAX_HZ, self.processor.feature.fps, order=5)
            self.bvp_r = butterworth_filter(self.processor.polynomialize(self.bvp_r),
                                            MIN_HZ, MAX_HZ, self.processor.feature.fps, order=5)

            self.spec_f = np.abs(np.fft.fft(self.bvp_f))
            self.spec_l = np.abs(np.fft.fft(self.bvp_l))
            self.spec_r = np.abs(np.fft.fft(self.bvp_r))

            self.bpm_f = self.processor.transfer2bpm(self.bpm_f, self.spec_f, self.conf_f)
            self.bpm_l = self.processor.transfer2bpm(self.bpm_l, self.spec_l, self.conf_l)
            self.bpm_r = self.processor.transfer2bpm(self.bpm_r, self.spec_r, self.conf_r)

        self.total_conf = self.conf_f + self.conf_l + self.conf_r
        self.weight_f = self.conf_f / self.total_conf
        self.weight_l = self.conf_l / self.total_conf
        self.weight_r = self.conf_r / self.total_conf

        self.bpm_avg = self.bpm_f * self.weight_f + self.bpm_l * self.weight_l + self.bpm_r * self.weight_r
        print(self.bpm_avg)

if __name__ == "__main__":
    main = Main()
    while True:
        bpm = main.DisplayBpm()
        print(main.processor.feature.flag_queue)
        # print(main.bpm_avg)
