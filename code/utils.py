import base64
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import cv2 as cv

import options  
kwargs = options.get_options()

def butterworth_filter(stream, low, high, sample_rate, order=11):
    nyquist_rate = sample_rate * 0.5
    low /= nyquist_rate
    high /= nyquist_rate
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.lfilter(b, a, stream)

def RGB_hist(roi):
    b_hist = cv.calcHist([roi], [0], None, [256], [0, 256])
    g_hist = cv.calcHist([roi], [1], None, [256], [0, 256])
    r_hist = cv.calcHist([roi], [2], None, [256], [0, 256])

    b_hist = np.reshape(b_hist, (256))
    g_hist = np.reshape(g_hist, (256))
    r_hist = np.reshape(r_hist, (256))

    b_hist[0] = 0
    g_hist[0] = 0
    r_hist[0] = 0

    r_hist = r_hist/np.sum(r_hist)
    g_hist = g_hist/np.sum(g_hist)
    b_hist = b_hist/np.sum(b_hist)

    return [r_hist, g_hist, b_hist]

def Hist2Feature(hist):
    hist_r = hist[0]
    hist_g = hist[1]
    hist_b = hist[2]

    hist_r /= np.sum(hist_r)
    hist_g /= np.sum(hist_g)
    hist_b /= np.sum(hist_b)

    dens = np.arange(0, 256, 1)
    mean_r = dens.dot(hist_r)
    mean_g = dens.dot(hist_g)
    mean_b = dens.dot(hist_b)

    return [mean_r, mean_g, mean_b]
