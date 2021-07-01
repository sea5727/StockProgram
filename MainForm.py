
import sys
from functools import partial
from PyQt5 import QtWidgets
from PyQt5 import QAxContainer

from kiwoom import Kiwoom
from ForeignerTradeTopForm import ForeignerTradeTopForm
from NewHighLowForm import NewHighLowForm

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

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.btnLogin)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

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
            form.exec_()
            Kiwoom.getInstance().viewnum.append(form.viewnum)
        elif text == '신고저가요청':
            viewnum = Kiwoom.getInstance().viewnum.pop(0)
            form = NewHighLowForm(viewnum)
            form.exec_()
            Kiwoom.getInstance().viewnum.append(form.viewnum)
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