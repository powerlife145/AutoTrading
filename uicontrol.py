import time

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import *

AUTO_TRADE_TERM = 1 #자동 매매 시도 간격, 초 단위
class uicontrol():
    def __init__(self, context):
        self.context = context
        context.lineEdit.textChanged.connect(self.code_changed)
        context.lineEdit_3.setText(context.kiwoom.server)

        accouns_num = int(context.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = context.kiwoom.get_login_info("ACCNO")
        accounts_list = accounts.split(';')[0:accouns_num]
        context.comboBox.addItems(accounts_list)
        context.pushButton.clicked.connect(self.send_order)
        context.pushButton_2.clicked.connect(self.check_balance)

        context.pushButton_3.clicked.connect(self.filter_codes)
        context.lineEdit_4.returnPressed.connect(self.filter_codes)
        context.listWidget.itemClicked.connect(self.select_code)
        context.tableWidget_2.cellClicked.connect(self.select_code2)

        context.pushButton_4.clicked.connect(self.control_auto_trade)
        context.uitimer.add_timer(AUTO_TRADE_TERM, self.auto_trade) #자동 매매 타이머

        self.searched_code_list = {}
        self.searched_name_list = {}

    def code_changed(self):
        code = self.context.lineEdit.text()
        name = self.context.kiwoom.get_master_code_name(code)
        self.context.lineEdit_2.setText(name)

    def filter_codes(self):
        keyword = self.context.lineEdit_4.text()
        m_code = self.context.comboBox_5.currentText()
        self.searched_code_list = dict(filter(lambda e: keyword.upper() in e[1].upper(), self.context.kiwoom.stock_name_list[m_code].items()))
        self.context.listWidget.clear()
        for code, name in self.searched_code_list.items():
            self.context.listWidget.addItem(name)
            self.searched_name_list[name] = code

    def select_code(self):
        name = self.context.listWidget.currentItem().text()
        code = self.searched_name_list[name]
        self.context.lineEdit.setText(code)
        self.context.pychart.display_chart(code)
        self.context.webreader.diplay_fin_inform(code)

    def select_code2(self):
        name = self.context.tableWidget_2.item(self.context.tableWidget_2.currentRow(), 0).text()

        for _, code_list in self.context.kiwoom.stock_name_list.items():
            selected_code = dict(filter(lambda e: name == e[1], code_list.items()))
            if any(selected_code):
                break

        code = str(list(selected_code.keys())[0])
        self.context.lineEdit.setText(code)
        self.context.pychart.display_chart(code)
        self.context.webreader.diplay_fin_inform(code)

    def send_order(self):
        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소': 4}
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        account = self.context.comboBox.currentText()
        order_type = self.context.comboBox_2.currentText()
        code = self.context.lineEdit.text()
        hoga = self.context.comboBox_3.currentText()
        num = self.context.spinBox.value()
        price = self.context.spinBox_2.value()

        self.context.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price,
                               hoga_lookup[hoga], "")

    def check_balance(self):
        self.context.kiwoom.reset_opw00018_output()
        account_number = self.context.kiwoom.get_login_info("ACCNO")
        account_number = account_number.split(';')[0]

        self.context.kiwoom.set_input_value("계좌번호", account_number)
        self.context.kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000", lambda: 1)

        while self.context.kiwoom.remained_data:
            time.sleep(0.2)
            self.context.kiwoom.set_input_value("계좌번호", account_number)
            self.context.kiwoom.comm_rq_data("opw00018_req", "opw00018", 2, "2000", lambda: 1)

        # opw00001
        self.context.kiwoom.set_input_value("계좌번호", account_number)
        self.context.kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000", lambda: 1)

        # balance
        item = QTableWidgetItem(self.context.kiwoom.d2_deposit)
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.context.tableWidget.setItem(0, 0, item)

        for i in range(1, 6):
            item = QTableWidgetItem(self.context.kiwoom.opw00018_output['single'][i - 1])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.context.tableWidget.setItem(0, i, item)

        self.context.tableWidget.resizeRowsToContents()

        # Item list
        item_count = len(self.context.kiwoom.opw00018_output['multi'])
        self.context.tableWidget_2.setRowCount(item_count)

        for j in range(item_count):
            row = self.context.kiwoom.opw00018_output['multi'][j]
            for i in range(len(row)):
                item = QTableWidgetItem(row[i])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.context.tableWidget_2.setItem(j, i, item)

        self.context.tableWidget_2.resizeRowsToContents()

    def auto_trade(self):
        if self.context.lineEdit_5.text() != "":
            con_name = self.context.comboBox_4.currentText()
            self.context.strategy.trade_by_condition(con_name)

    def control_auto_trade(self):
        if self.context.lineEdit_5.text() == "":
            self.context.lineEdit_5.setText(" 자동 매매 중...")
            self.context.lineEdit_5.setStyleSheet("color: red;background-color:rgb(255, 255, 127);")
            self.context.pushButton_4.setText("자동 매매 중지")

            con_name = self.context.comboBox_4.currentText()
            self.context.comboBox_4.setEnabled(False)
            self.context.textEdit.setText(f'{con_name}을 사용하여 현재 자동 매매 중입니다.\n자동매매 주기는 {str(AUTO_TRADE_TERM)}초 입니다.')

        else:
            self.context.lineEdit_5.setText("")
            self.context.lineEdit_5.setStyleSheet("")
            self.context.pushButton_4.setText("자동 매매 시작")
            self.context.comboBox_4.setEnabled(True)
