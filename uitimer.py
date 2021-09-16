from PyQt5.QtCore import QTimer, QTime


class uitimer():
    def __init__(self, context):
        self.context = context
        self.timer = QTimer(context)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

        self.timer2 = QTimer(context)
        self.timer2.start(1000 * 2) #10초에 한번씩 업데이트
        self.timer2.timeout.connect(self.timeout2)
        self.timer_list = []
        self.call_list = []

    def timeout(self):
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        state = self.context.kiwoom.get_connect_state()
        if state == 1:
            state_msg = "서버 연결 중"
        else:
            state_msg = "서버 미 연결 중"

        self.context.statusbar.showMessage(state_msg + " | " + time_msg)

    def timeout2(self):
        if self.context.checkBox.isChecked():
            self.context.uicontrol.check_balance()

    def add_timer(self, dt, callback):
        self.timer_list.append(QTimer(self.context))
        self.call_list.append(callback)
        n = len(self.timer_list)
        self.timer_list[n-1].start(1000*dt)

        self.call_list[n - 1]()
        self.timer_list[n-1].timeout.connect(self.call_list[n-1])


