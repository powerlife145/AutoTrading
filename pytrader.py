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
from strategy import *

form_class = uic.loadUiType("pytrader.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()
        self.uitimer = uitimer(self)
        self.uicontrol = uicontrol(self) # 타이머를 사용하므로 타이머 보다 나중에 실행되야 함.

        # 아래 클래스들은 UI를 사용하므로 uicontrol보다 나중에 실행되어야 함.
        self.pychart = pychart(self)
        self.webreader = webreader(self)
        self.strategy = strategy(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()