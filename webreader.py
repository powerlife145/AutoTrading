import requests
import re
import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from bs4 import BeautifulSoup
from dateutil.parser import parse
import datetime
from PyQt5.QtCore import *

class webreader():
    def __init__(self, context):
        self.context = context

    def get_financial_statements(self, code):
        re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
        re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)

        url = "http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={}".format(code)
        html = requests.get(url).text
        encparam = re_enc.search(html).group(1)
        encid = re_id.search(html).group(1)

        url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ=A&encparam={}&id={}".format(code, encparam, encid)
        headers = {"Referer": "HACK"}
        html = requests.get(url, headers=headers).text

        dfs = pd.read_html(html.replace("(IFRS별도)", "").replace("(E)","").replace("(IFRS연결)",""))
        df = dfs[1]['연간연간컨센서스보기']
        df.index = dfs[1]['주요재무정보'].values.flatten()
        # df = df.loc['현금배당수익률']
        # df.index = df.index.str[:7]
        return df

    def get_3year_treasury(self):
        # url = "http://www.index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=288401&amp;idx_cd=2884&amp;freq=Y&amp;period=1998:2021"
        start_year = 1997
        end_year = datetime.datetime.now().year-1

        url ="https://www.index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=107301&idx_cd=1073&freq=Y&period="+str(start_year)+":"+str(end_year)
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')
        td_data = soup.select("tr td")

        treasury_3year = {}

        for x in td_data:
            treasury_3year[start_year] = x.text
            start_year += 1
            if start_year>end_year:
                break

        # print(treasury_3year)
        return treasury_3year

    def get_dividend_yield(self, code):
        url = "http://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd=" + code
        html = requests.get(url).text

        soup = BeautifulSoup(html, 'html5lib')
        dt_data = soup.select("td dl dt")

        dividend_yield = dt_data[-2].text
        dividend_yield = dividend_yield.split(' ')[1]
        dividend_yield = dividend_yield[:-1]

        return dividend_yield

    def get_estimated_dividend_yield(self, code):
        dividend_yield = self.get_financial_statements(code).loc['현금배당수익률']
        print(dividend_yield)
        dividend_yield = sorted(dividend_yield.items())[-1]
        print(dividend_yield)
        print(dividend_yield[1])
        return dividend_yield[1]

    def get_current_3year_treasury(self):
        url = "http://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page=1"
        html = requests.get(url).text

        soup = BeautifulSoup(html, 'html5lib')
        td_data = soup.select("tr td")
        return td_data[1].text

    def get_previous_dividend_yield(self,code):
        dividend_yield = self.get_financial_statements(code).loc['현금배당수익률']

        dividend_yield.index = list(map(lambda x: parse(x).year, dividend_yield.index))
        now = datetime.datetime.now()
        cur_year = now.year
        previous_dividend_yield = {}

        for year in range(cur_year-5, cur_year):

            if year in dividend_yield.index:
                previous_dividend_yield[year] = dividend_yield[year]

        return previous_dividend_yield

    def calculate_estimated_dividend_to_treasury(self, code):
        estimated_dividend_yield = self.get_estimated_dividend_yield(code)
        current_3year_treasury = self.get_current_3year_treasury()
        estimated_dividend_to_treasury = float(estimated_dividend_yield) / float(current_3year_treasury)
        return estimated_dividend_to_treasury

    def get_min_max_dividend_to_treasury(self, code):
        previous_dividend_yield = self.get_previous_dividend_yield(code)
        three_years_treasury = self.get_3year_treasury()

        now = datetime.datetime.now()
        cur_year = now.year
        previous_dividend_to_treasury = {}

        for year in range(cur_year-5, cur_year):
            if year in previous_dividend_yield.keys() and year in three_years_treasury.keys():
                ratio = float(previous_dividend_yield[year]) / float(three_years_treasury[year])
                previous_dividend_to_treasury[year] = ratio

        print(previous_dividend_to_treasury)
        min_ratio = min(previous_dividend_to_treasury.values())
        max_ratio = max(previous_dividend_to_treasury.values())

        return min_ratio, max_ratio

    def diplay_fin_inform(self, code):

        fin_data = self.get_financial_statements(code)
        self.context.tableWidget_4.setRowCount(len(fin_data.index))
        self.context.tableWidget_4.setColumnCount(len(fin_data.columns))
        self.context.tableWidget_4.setHorizontalHeaderLabels(fin_data.columns)
        self.context.tableWidget_4.setVerticalHeaderLabels(fin_data.index)

        font = self.context.tableWidget_4.horizontalHeader().font()
        font.setPointSize(10)
        font.setBold(True)
        self.context.tableWidget_4.verticalHeader().setFont(font)
        self.context.tableWidget_4.horizontalHeader().setFont(font)

        for i in range(0,len(fin_data.index)):
            for j in range(0, len(fin_data.columns)):
                # item = QTableWidgetItem(fin_data[i][j])
                item = QTableWidgetItem(str(fin_data.iat[i, j]))

                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.context.tableWidget_4.setItem(i, j, item)

        self.context.tableWidget_4.resizeRowsToContents()
        self.context.tableWidget_4.resizeColumnsToContents()

        header = self.context.tableWidget_4.horizontalHeader()
        twidth = header.width()
        width = []
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
            width.append(header.sectionSize(column))

        wfactor = twidth / sum(width)
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.Interactive)
            header.resizeSection(column, width[column]*wfactor)