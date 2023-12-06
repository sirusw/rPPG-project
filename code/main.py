import time

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

class Main():
    def __init__(self):
        self.processor = feature2rppg()
        self.processor.streaming()
        self.mode = self.processor.Chrom

        self.bpm_f, self.bpm_l, self.bpm_r = 60, 60, 60
        self.bpm_avg = 60
    
    def DisplayBpm(self):
        signal_f = np.array(self.processor.feature.sig_fore)
        # signal_l = np.array(self.processor.feature.sig_left)
        # signal_r = np.array(self.processor.feature.sig_right)

        if self.processor.feature.flag_queue:
            if signal_f.size != 1:
                self.bvp_f = self.mode(signal_f)
                self.convince_f = 1 / \
                    (max(self.bvp_f) - min(self.bvp_f))
                self.bvp_f = butterworth_filter(self.processor.polynomialize(self.bvp_f), 
                                                MIN_HZ, MAX_HZ, self.processor.feature.fps, order=5)

                self.spec_f = np.abs(np.fft.fft(self.bvp_f))
                self.bpm_f = self.processor.transfer2bpm(self.bpm_f, self.spec_f, self.convince_f)
        return self.bpm_f

if __name__ == "__main__":
    main = Main()
    bpm = main.DisplayBpm()
    print(bpm)

