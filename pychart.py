
from PyQt5.QtChart import QLineSeries, QChart, QDateTimeAxis, QValueAxis, QCandlestickSet, QCandlestickSeries
from PyQt5.QtGui import QPainter
# from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from PyQt5 import uic
# from matplotlib import ticker
from pandas import DataFrame, Series
from dateutil.parser import parse

class pychart():
    def __init__(self, context):
        self.context = context


    def display_chart(self, code):

        self.priceChart = QChart()
        self.priceChart.legend().hide()
        self.series = QCandlestickSeries()
        self.series.setIncreasingColor(Qt.red)
        self.series.setDecreasingColor(Qt.blue)
        self.series.setBodyOutlineVisible(False)

        self.context.kiwoom.set_input_value("종목코드", code)
        self.context.kiwoom.set_input_value("틱범위", "1")
        self.context.kiwoom.set_input_value("수정주가구분", 1)
        self.context.kiwoom.comm_rq_data("opt10080_req", "opt10080", 0, "0101", self.update_price_minute)

    def update_price_minute(self, val):

        df = DataFrame(val, columns=['open', 'high', 'low', 'close', 'volume'],
                           index=val['tick'])

        for index in df.index[0:180]:
            open = abs(df.loc[index, 'open'])
            high = abs(df.loc[index, 'high'])
            low = abs(df.loc[index, 'low'])
            close = abs(df.loc[index, 'close'])

            # time conversion
            format = "%Y-%m-%d %H:%M:%S"
            str_time = parse(index).strftime(format)
            dt = QDateTime.fromString(str_time, "yyyy-MM-dd hh:mm:ss")
            ts = dt.toMSecsSinceEpoch()

            elem = QCandlestickSet(open, high, low, close, ts)
            self.series.append(elem)

        self.priceChart.addSeries(self.series)

        axisX = QDateTimeAxis()
        axisX.setFormat("hh:mm")
        self.priceChart.addAxis(axisX, Qt.AlignBottom)
        axisX.setTickCount(15)

        self.series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setLabelFormat("%i")
        self.priceChart.addAxis(axisY, Qt.AlignLeft)
        self.series.attachAxis(axisY)

        self.priceChart.layout().setContentsMargins(0, 0, 0, 0)

        self.context.priceView.setChart(self.priceChart)
        self.context.priceView.setRenderHints(QPainter.Antialiasing)
