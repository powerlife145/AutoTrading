import sys

from PyQt5.QtChart import QLineSeries, QChart, QDateTimeAxis, QValueAxis, QCandlestickSet, QCandlestickSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from matplotlib import ticker
from pandas import DataFrame, Series
from dateutil.parser import parse

from Kiwoom import *
from uitimer import *
from uicontrol import *
from pychart import *
from webreader import *
form_class = uic.loadUiType("pytrader.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()
        self.uitimer = uitimer(self)
        self.uicontrol = uicontrol(self)
        self.pychart = pychart(self)
        self.webreader = webreader(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()