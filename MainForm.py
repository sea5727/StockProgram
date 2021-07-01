

from Form.SamePurchaseRankForm import SamePurchaseRankForm
import sys
from functools import partial
from PyQt5 import QtWidgets
from PyQt5 import QAxContainer

from kiwoom import Kiwoom
from Form.TradingVolumeSoarForm import TradingVolumeSoarForm
from Form.ForeignerTradeTopForm import ForeignerTradeTopForm
from Form.NewHighLowForm import NewHighLowForm
from Form.MarketTopPerInvestorForm import MarketTopPerInvestorForm

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.kiwoom = Kiwoom.getInstance()

        self.setWindowTitle("StockProgram")
        self.setGeometry(100, 100, 300, 100)

        self.btnLogin = QtWidgets.QPushButton("Login", self)
        self.btnLogin.clicked.connect(self.on_clicked_btnLogin)

        self.btn1 = QtWidgets.QPushButton("외국인매매상위요청", self)
        self.btn1.clicked.connect(partial(self.on_clicked, self.btn1.text()))

        self.btn2 = QtWidgets.QPushButton("신고저가요청", self)
        self.btn2.clicked.connect(partial(self.on_clicked, self.btn2.text()))

        self.btn3 = QtWidgets.QPushButton("거래량급증요청", self)
        self.btn3.clicked.connect(partial(self.on_clicked, self.btn3.text()))

        self.btn4 = QtWidgets.QPushButton("장중투자자별매매상위요청", self)
        self.btn4.clicked.connect(partial(self.on_clicked, self.btn4.text()))

        self.btn5 = QtWidgets.QPushButton("동일순매매순위요청", self)
        self.btn5.clicked.connect(partial(self.on_clicked, self.btn5.text()))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.btnLogin)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        layout.addWidget(self.btn4)
        layout.addWidget(self.btn5)

        self.setLayout(layout)


    def on_clicked_btnLogin(self):
        '''
        '''
        ret = self.kiwoom.login()
        if ret != 0:
            QtWidgets.QMessageBox.about(self, "Error", "로그인 실행 실패")
    
    def on_clicked(self, text):
        '''
        '''
        
        if text == '외국인매매상위요청':
            viewnum = Kiwoom.getInstance().viewnum.pop(0)
            form = ForeignerTradeTopForm(viewnum)
            form.show()
        elif text == '신고저가요청':
            viewnum = Kiwoom.getInstance().viewnum.pop(0)
            form = NewHighLowForm(viewnum)
            form.show()
        elif text == '거래량급증요청':
            viewnum = Kiwoom.getInstance().viewnum.pop(0)
            form = TradingVolumeSoarForm(viewnum)
            form.show()
        elif text == '장중투자자별매매상위요청':
            viewnum = Kiwoom.getInstance().viewnum.pop(0)
            form = MarketTopPerInvestorForm(viewnum)
            form.show()
        elif text == '동일순매매순위요청':
            viewnum = Kiwoom.getInstance().viewnum.pop(0)
            form = SamePurchaseRankForm(viewnum)
            form.show()
        else: 
            return

class MainForm(QtWidgets.QMainWindow):
    def __init__(self):
        '''
        '''
        super().__init__()

        self.kiwoom = Kiwoom.getInstance()

        mainform = MainWidget()
        self.setCentralWidget(mainform)

        self.setWindowTitle("StockProgram")
        self.setGeometry(100, 100, 300, 100)       


        

def on_clicked_login():
    '''
    '''

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainform = MainForm()
    mainform.show()

    app.exec_()
    print('after event loop')