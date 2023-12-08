from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg

import os
import sys
import time
import numpy as np
import cv2 as cv

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import django

from core import feature2rppg
from utils import butterworth_filter

MIN_HZ = 0.85  # 51bpm
MAX_HZ = 2.5  # 150bpm
BETA = 0.95  # smoothing factor


class ui(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1308, 850)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.face = QtWidgets.QLabel(self.centralwidget)
        self.face.setGeometry(QtCore.QRect(620, 10, 681, 391))
        self.face.setText("")
        self.face.setObjectName("face")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 410, 531, 431))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Layout_BVP = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Layout_BVP.setContentsMargins(0, 0, 0, 0)
        self.Layout_BVP.setObjectName("Layout_BVP")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 601, 391))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.Layout_button = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.Layout_button.setContentsMargins(0, 0, 0, 0)
        self.Layout_button.setObjectName("Layout_button")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 28))
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 28))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.Layout_button.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Button_RawTrue = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.Button_RawTrue.setObjectName("Button_RawTrue")
        self.horizontalLayout_2.addWidget(self.Button_RawTrue)
        self.Button_RawFalse = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.Button_RawFalse.setObjectName("Button_RawFalse")
        self.horizontalLayout_2.addWidget(self.Button_RawFalse)
        self.Layout_button.addLayout(self.horizontalLayout_2)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setMinimumSize(QtCore.QSize(0, 300))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        )
        self.label.setObjectName("label")
        self.Layout_button.addWidget(self.label)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(890, 410, 411, 431))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.Layout_Signal = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.Layout_Signal.setContentsMargins(0, 0, 0, 0)
        self.Layout_Signal.setObjectName("Layout_Signal")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(550, 410, 331, 431))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.Layout_Spec = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.Layout_Spec.setContentsMargins(0, 0, 0, 0)
        self.Layout_Spec.setObjectName("Layout_Spec")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox.setItemText(0, _translate("MainWindow", "CHROM"))
        self.Button_RawTrue.setText(_translate("MainWindow", "Raw Signal"))
        self.Button_RawFalse.setText(_translate("MainWindow", "Filtered Signal"))


class Procedure(QMainWindow, ui):
    def __init__(self, parent=None):
        super(Procedure, self).__init__(parent)
        self.setupUi(self)

        self.Hist_f = pg.PlotWidget(self)
        self.Hist_l = pg.PlotWidget(self)
        self.Hist_r = pg.PlotWidget(self)

        self.Hist_f.setYRange(0, 0.2)
        self.Hist_l.setYRange(0, 0.2)
        self.Hist_r.setYRange(0, 0.2)

        self.label_f = QLabel(self.verticalLayoutWidget)
        self.label_l = QLabel(self.verticalLayoutWidget)
        self.label_r = QLabel(self.verticalLayoutWidget)
        self.Hist_f_r = self.Hist_f.plot()
        self.Hist_f_g = self.Hist_f.plot()
        self.Hist_f_b = self.Hist_f.plot()
        self.Hist_l_r = self.Hist_l.plot()
        self.Hist_l_g = self.Hist_l.plot()
        self.Hist_l_b = self.Hist_l.plot()
        self.Hist_r_r = self.Hist_r.plot()
        self.Hist_r_g = self.Hist_r.plot()
        self.Hist_r_b = self.Hist_r.plot()
        self.Layout_Signal.addWidget(self.Hist_f)
        self.Layout_Signal.addWidget(self.Hist_l)
        self.Layout_Signal.addWidget(self.Hist_r)

        self.Signal_f = pg.PlotWidget(self)
        self.Signal_l = pg.PlotWidget(self)
        self.Signal_r = pg.PlotWidget(self)

        self.Sig_f = self.Signal_f.plot()
        self.Sig_l = self.Signal_l.plot()
        self.Sig_r = self.Signal_r.plot()

        self.Spectrum_f = pg.PlotWidget(self)
        self.Spectrum_l = pg.PlotWidget(self)
        self.Spectrum_r = pg.PlotWidget(self)

        self.Spec_f = self.Spectrum_f.plot()
        self.Spec_l = self.Spectrum_l.plot()
        self.Spec_r = self.Spectrum_r.plot()

        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.label_f.setFont(font)
        self.label_f.setText("Forehead Signal")
        self.Layout_BVP.addWidget(self.label_f)

        self.Layout_BVP.addWidget(self.Signal_f)

        self.label_l.setFont(font)
        self.label_l.setText("Left Cheek Signal")
        self.Layout_BVP.addWidget(self.label_l)

        self.Layout_BVP.addWidget(self.Signal_l)

        self.label_r.setFont(font)
        self.label_r.setText("Right Cheek Signal")
        self.Layout_BVP.addWidget(self.label_r)

        self.Layout_BVP.addWidget(self.Signal_r)

        self.Layout_Spec.addWidget(self.Spectrum_f)
        self.Layout_Spec.addWidget(self.Spectrum_l)
        self.Layout_Spec.addWidget(self.Spectrum_r)

        self.face.setScaledContents(True)

        self.processor = feature2rppg()
        self.processor.streaming()

        self.TIMER_Frame = QTimer()
        self.TIMER_Frame.setInterval(100)
        self.TIMER_Frame.start()

        self.TIMER_Hist = QTimer()
        self.TIMER_Hist.setInterval(100)
        self.TIMER_Hist.start()

        self.TIMER_SIGNAL = QTimer()
        self.TIMER_SIGNAL.setInterval(100)
        self.TIMER_SIGNAL.start()

        self.bpm_f = 60
        self.bpm_l = 60
        self.bpm_r = 60

        self.bpm_avg = 60
        self.ModeDict = {"CHROM": self.processor.CHROM}
        self.Mode = self.ModeDict["CHROM"]
        self.Data_ShowRaw = True
        self.slot_init()

        self.start_time_hr = time.time()
        self.start_time_sp = time.time()

        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        django_project_directory = os.path.join(parent_directory, "server")
        print(django_project_directory)
        sys.path.insert(0, django_project_directory)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
        django.setup()
        self.channel_layer = get_channel_layer()

    def slot_init(self):
        self.TIMER_Frame.timeout.connect(self.DisplayImage)
        self.TIMER_Hist.timeout.connect(self.DisplayHist)
        self.TIMER_SIGNAL.timeout.connect(self.DisplaySignal)
        self.comboBox.activated[str].connect(self.Button_ChangeMode)
        self.Button_RawTrue.clicked.connect(self.Button_Data_RawTrue)
        self.Button_RawFalse.clicked.connect(self.Button_Data_RawFalse)

    def Button_ChangeMode(self, str):
        self.Mode = self.ModeDict[str]

    def Button_Data_RawTrue(self):
        self.Data_ShowRaw = True

    def Button_Data_RawFalse(self):
        self.Data_ShowRaw = False

    def DisplayImage(self):
        Mask = self.processor.series_class.face_mask
        Mask = cv.ellipse(
            Mask, [640, 360], [80, 120], 0, 0, 360, [0, 255, 0], 1, cv.LINE_AA
        )
        Mask = cv.circle(Mask, [640, 360], 2, [255, 0, 0], 2, cv.LINE_AA)

        if Mask is not None:
            img = cv.cvtColor(Mask, cv.COLOR_BGR2RGB)
            qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)

            self.face.setPixmap(QPixmap.fromImage(qimg))

    def DisplayHist(self):
        Hist_f = np.array(self.processor.series_class.hist_f)
        Hist_l = np.array(self.processor.series_class.hist_l)
        Hist_r = np.array(self.processor.series_class.hist_r)
        if Hist_f.size != 1:
            self.Hist_f_r.setData(Hist_f[0, :], pen=(255, 0, 0))
            self.Hist_f_g.setData(Hist_f[1, :], pen=(0, 255, 0))
            self.Hist_f_b.setData(Hist_f[2, :], pen=(0, 0, 255))
        else:
            self.Hist_f_r.clear()
            self.Hist_f_g.clear()
            self.Hist_f_b.clear()
        if Hist_l.size != 1:
            self.Hist_l_r.setData(Hist_l[0, :], pen=(255, 0, 0))
            self.Hist_l_g.setData(Hist_l[1, :], pen=(0, 255, 0))
            self.Hist_l_b.setData(Hist_l[2, :], pen=(0, 0, 255))
        else:
            self.Hist_l_r.clear()
            self.Hist_l_g.clear()
            self.Hist_l_b.clear()
        if Hist_f.size != 1:
            self.Hist_r_r.setData(Hist_r[0, :], pen=(255, 0, 0))
            self.Hist_r_g.setData(Hist_r[1, :], pen=(0, 255, 0))
            self.Hist_r_b.setData(Hist_r[2, :], pen=(0, 0, 255))
        else:
            self.Hist_r_r.clear()
            self.Hist_r_g.clear()
            self.Hist_r_b.clear()

        Hist_f_r_data_x, Hist_f_r_data_y = self.Hist_f_r.getData()
        Hist_f_g_data_x, Hist_f_g_data_y = self.Hist_f_g.getData()
        Hist_f_b_data_x, Hist_f_b_data_y = self.Hist_f_b.getData()

        Hist_l_r_data_x, Hist_l_r_data_y = self.Hist_l_r.getData()
        Hist_l_g_data_x, Hist_l_g_data_y = self.Hist_l_g.getData()
        Hist_l_b_data_x, Hist_l_b_data_y = self.Hist_l_b.getData()

        Hist_r_r_data_x, Hist_r_r_data_y = self.Hist_r_r.getData()
        Hist_r_g_data_x, Hist_r_g_data_y = self.Hist_r_g.getData()
        Hist_r_b_data_x, Hist_r_b_data_y = self.Hist_r_b.getData()
        current_time_sp = time.time()
        elapsed_time_sp = current_time_sp - self.start_time_sp
        if elapsed_time_sp >= 2:
            async_to_sync(self.channel_layer.group_send)(
                "video",
                {
                    "type": "video.sp",
                    "sp_f": [
                        [Hist_f_r_data_x.tolist(), Hist_f_r_data_y.tolist()],
                        [Hist_f_g_data_x.tolist(), Hist_f_g_data_y.tolist()],
                        [Hist_f_b_data_x.tolist(), Hist_f_b_data_y.tolist()],
                    ],
                    "sp_l": [
                        [Hist_l_r_data_x.tolist(), Hist_l_r_data_y.tolist()],
                        [Hist_l_g_data_x.tolist(), Hist_l_g_data_y.tolist()],
                        [Hist_l_b_data_x.tolist(), Hist_l_b_data_y.tolist()],
                    ],
                    "sp_r": [
                        [Hist_r_r_data_x.tolist(), Hist_r_r_data_y.tolist()],
                        [Hist_r_g_data_x.tolist(), Hist_r_g_data_y.tolist()],
                        [Hist_r_b_data_x.tolist(), Hist_r_b_data_y.tolist()],
                    ],
                },
            )
            self.start_time_sp = current_time_sp

    def DisplaySignal(self):
        Sig_f = np.array(self.processor.series_class.Sig_f)
        Sig_l = np.array(self.processor.series_class.Sig_l)
        Sig_r = np.array(self.processor.series_class.Sig_r)
        if self.processor.series_class.flag_Queue:
            if Sig_f.size != 1:
                # self.bvp_f_raw = self.processor.PBV(Sig_f)
                self.bvp_f_raw = self.Mode(Sig_f)
                self.conf_f = 1 / (max(self.bvp_f_raw) - min(self.bvp_f_raw))
                self.bvp_f = butterworth_filter(
                    self.processor.Signal_Preprocessing_single(self.bvp_f_raw),
                    MIN_HZ,
                    MAX_HZ,
                    self.processor.series_class.fps,
                    order=5,
                )
                self.spc_f = np.abs(np.fft.fft(self.bvp_f))
                self.bpm_f = self.processor.transfer2bmp(
                    BETA, self.bpm_f, self.spc_f, self.processor.series_class.fps
                )
                if self.Data_ShowRaw:
                    self.Sig_f.setData(self.bvp_f_raw, pen=(0, 255, 255))
                else:
                    self.Sig_f.setData(self.bvp_f, pen=(0, 255, 255))
                self.Spec_f.setData(
                    np.linspace(
                        0,
                        self.processor.series_class.fps / 2 * 60,
                        int((len(self.spc_f) + 1) / 2),
                    ),
                    self.spc_f[: int((len(self.spc_f) + 1) / 2)],
                    pen=(0, 255, 255),
                )
            else:
                self.Sig_f.setData([0], [0])
                self.Spec_f.setData([0], [0])
            if Sig_l.size != 1:
                # self.bvp_l_raw = self.processor.GREEN(Sig_l)
                self.bvp_l_raw = self.Mode(Sig_l)
                self.conf_l = 1 / (max(self.bvp_l_raw) - min(self.bvp_l_raw))
                self.bvp_l = butterworth_filter(
                    self.processor.Signal_Preprocessing_single(self.bvp_l_raw),
                    MIN_HZ,
                    MAX_HZ,
                    self.processor.series_class.fps,
                    order=5,
                )
                self.spc_l = np.abs(np.fft.fft(self.bvp_l))
                self.bpm_l = self.processor.transfer2bmp(
                    BETA, self.bpm_l, self.spc_l, self.processor.series_class.fps
                )
                if self.Data_ShowRaw:
                    self.Sig_l.setData(self.bvp_l_raw, pen=(255, 0, 255))
                else:
                    self.Sig_l.setData(self.bvp_l, pen=(255, 0, 255))
                self.Spec_l.setData(
                    np.linspace(
                        0,
                        self.processor.series_class.fps / 2 * 60,
                        int((len(self.spc_l) + 1) / 2),
                    ),
                    self.spc_l[: int((len(self.spc_l) + 1) / 2)],
                    pen=(255, 0, 255),
                )
            else:
                self.Sig_l.setData([0], [0])
                self.Spec_l.clear([0], [0])
            if Sig_r.size != 1:
                # self.bvp_r_raw = self.processor.CHROM(Sig_r)
                self.bvp_r_raw = self.Mode(Sig_r)
                self.conf_r = 1 / (max(self.bvp_r_raw) - min(self.bvp_r_raw))
                self.bvp_r = butterworth_filter(
                    self.processor.Signal_Preprocessing_single(self.bvp_r_raw),
                    MIN_HZ,
                    MAX_HZ,
                    self.processor.series_class.fps,
                    order=5,
                )
                self.spc_r = np.abs(np.fft.fft(self.bvp_r))
                self.bpm_r = self.processor.transfer2bmp(
                    BETA, self.bpm_r, self.spc_r, self.processor.series_class.fps
                )
                if self.Data_ShowRaw:
                    self.Sig_r.setData(self.bvp_r_raw, pen=(255, 255, 0))
                else:
                    self.Sig_r.setData(self.bvp_r, pen=(255, 255, 0))
                self.Spec_r.setData(
                    np.linspace(
                        0,
                        self.processor.series_class.fps / 2 * 60,
                        int((len(self.spc_r) + 1) / 2),
                    ),
                    self.spc_r[: int((len(self.spc_r) + 1) / 2)],
                    pen=(255, 255, 0),
                )
            else:
                self.Sig_r.setData([0], [0])
                self.Spec_r.setData([0], [0])

            self.total_conf = self.conf_f + self.conf_l + self.conf_r
            self.conf_f = self.conf_f / self.total_conf
            self.conf_l = self.conf_l / self.total_conf
            self.conf_r = self.conf_r / self.total_conf
            self.bpm_avg = (
                self.bpm_f * self.conf_f
                + self.bpm_l * self.conf_l
                + self.bpm_r * self.conf_r
            )

            current_time_hr = time.time()
            elapsed_time_hr = current_time_hr - self.start_time_hr
            if elapsed_time_hr >= 2:
                async_to_sync(self.channel_layer.group_send)(
                    "video",
                    {
                        "type": "video.hr",
                        "hr": self.bpm_avg,
                        "bpm_f": str(self.bpm_f),
                        "bpm_l": str(self.bpm_l),
                        "bpm_r": str(self.bpm_r),
                        "conf_f": str(self.conf_f * 100),
                        "conf_l": str(self.conf_l * 100),
                        "conf_r": str(self.conf_r * 100),
                    },
                )
                print("bpm ", self.bpm_avg)
                print("bpm_f ", self.bpm_f)
                print("bpm_l ", self.bpm_l)
                print("bpm_r ", self.bpm_r)
                print("conf_f ", self.conf_f)
                print("conf_l ", self.conf_l)
                print("conf_r ", self.conf_r)

                self.start_time_hr = current_time_hr

            Label_Text = (
                "Fs: \t\t"
                + str(self.processor.series_class.fps)
                + "\nFore BPM: \t"
                + str(self.bpm_f)
                + "\nFore Confidence: "
                + str(self.conf_f * 100)
                + "%\nLeft BPM: \t"
                + str(self.bpm_l)
                + "\nLeft Confidence: "
                + str(self.conf_l * 100)
                + "%\nRight BPM:\t"
                + str(self.bpm_r)
                + "\nRight Confidence:"
                + str(self.conf_r * 100)
                + "%\n\nBPM Overall: \t"
                + str(self.bpm_avg)
            )

            self.label.setText(Label_Text)
            print(Label_Text)

        else:
            self.Sig_f.setData([0], [0])
            self.Spec_f.setData([0], [0])
            self.Sig_l.setData([0], [0])
            self.Spec_l.setData([0], [0])
            self.Sig_r.setData([0], [0])
            self.Spec_r.setData([0], [0])
            self.label.setText(
                "Fs:\t\t" + str(self.processor.series_class.fps) + "\nCollecting..."
            )
