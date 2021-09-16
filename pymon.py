import sys
from PyQt5.QtWidgets import *
import Kiwoom
import time
from pandas import DataFrame

MARKET_KOSPI   = 0
MARKET_KOSDAQ  = 10

class PyMon:
    def __init__(self):
        self.kiwoom = Kiwoom.Kiwoom()
        self.kiwoom.comm_connect()
        self.get_code_list()

    def get_code_list(self):
        self.kospi_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSPI)
        self.kosdaq_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSDAQ)

    def get_ohlcv_day(self, code, start):
        self.kiwoom.ohlcv_day = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.set_input_value("기준일자", start)
        self.kiwoom.set_input_value("수정주가구분", 1)
        self.kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101", self.callbacktest)
        # time.sleep(0.2)
        #
        # df = DataFrame(self.kiwoom.ohlcv_day, columns=['open', 'high', 'low', 'close', 'volume'],
        #                index=self.kiwoom.ohlcv_day['date'])
        # return df

    # def get_ohlcv_min(self, code, start):
    #     self.kiwoom.ohlcv_min = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
    #
    #     self.kiwoom.set_input_value("종목코드", code)
    #     self.kiwoom.set_input_value("기준일자", start)
    #     self.kiwoom.set_input_value("수정주가구분", 1)
    #     self.kiwoom.comm_rq_data("opt10080_req", "opt10080", 0, "0101")
    #     time.sleep(0.2)
    #
    #     df = DataFrame(self.kiwoom.ohlcv_min, columns=['open', 'high', 'low', 'close', 'volume'],
    #                    index=self.kiwoom.ohlcv_min['date'])
    #     return df

    def callbacktest(self, val):
        df = DataFrame(val, columns=['open', 'high', 'low', 'close', 'volume'],
                           index=val['date'])
        print(df)


    def run(self):
        self.get_ohlcv_day("039490", "20170321")
        # df2 = self.get_ohlcv_min("039490", "60")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pymon = PyMon()
    pymon.run()
