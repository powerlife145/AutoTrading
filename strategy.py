from condition import *

class strategy:
    def __init__(self, context):
        self.context = context
        self.conditions = {}
        self.conditions['test1'] = condition()
        self.conditions['test2'] = condition()
        self.conditions['test3'] = condition()
        self.conditions['test4'] = condition()

        self.initialize()

    def initialize(self):
        for name, con in self.conditions.items():
            self.context.comboBox_4.addItem(name)

    def trade_by_condition(self, name):
        con = self.conditions[name]
        # buy_list = con.search_buy()
        # sell_list = con.search_sell()
        print(name)