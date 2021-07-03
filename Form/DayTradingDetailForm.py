import sys
sys.path.append("..")

from PyQt5 import QtWidgets
from kiwoom import Kiwoom
from ObserverImpl import OnRecieveTrDataEventObserver
from matplotlib import pyplot as plt
from Entity import Entity
from datetime import datetime

plt.rcParams["font.family"] = 'Malgun Gothic' 

class DayTradingDetailForm(QtWidgets.QDialog, OnRecieveTrDataEventObserver):
    def __init__(self, viewnum):
        '''
        '''
        super().__init__()

        self.viewnum = viewnum
        self.rqname = '일별거래상세요청'
        self.opt = 'OPT10015'

        self.isnext = 0

        self.setWindowTitle(self.rqname)
        self.resize(600, 600)
        
        self.txtStock = QtWidgets.QLineEdit()
        self.txtStock.setText('')

        self.txtDate = QtWidgets.QLineEdit()
        self.txtDate.setText(datetime.now().strftime('%Y%m%d'))

        self.btnSearch = QtWidgets.QPushButton()
        self.btnSearch.setText('조회')
        self.btnSearch.clicked.connect(self.on_clicked_btnSearch)

        self.result = QtWidgets.QTableWidget()
        self.columns = ['일자', '종가', '전일대비기호', '전일대비', '등락율', '거래량', '거래대금', 
            '장전거래량', '장전거래비중', '장중거래량', '장중거래비중', '장후거래량', '장후거래비중', 
            '합계3', '기간중거래량', '체결강도', '외인보유', '외인비중', '외인순매수', '기관순매수', 
            '개인순매수', '외국계', '신용잔고율', '프로그램', '장전거래대금', '장전거래대금비중', 
            '장중거래대금', '장중거래대금비중', '장후거래대금', '장후거래대금비중']
        
        self.result.setColumnCount(len(self.columns))
        self.result.setHorizontalHeaderLabels(self.columns)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.layout.addWidget(self.txtStock)
        self.layout.addWidget(self.txtDate)


        self.layout.addWidget(self.btnSearch)
        self.layout.addWidget(self.result)
        self.setLayout(self.layout)

        Kiwoom.getInstance().obs.AddObserver(self)
    
        # close event 처리
    def closeEvent(self, QCloseEvent):
        Kiwoom.getInstance().viewnum.append(self.viewnum)

        self.deleteLater()
        QCloseEvent.accept()

    def on_clicked_btnSearch(self):
        '''
        '''
        self.ProcOpenApi()


    def OnNotify(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        '''
        '''
        self.ProcResult(screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4)

    def ProcOpenApi(self):
        '''
        '''
        self.kiwoom = Kiwoom.getInstance()

        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '종목코드', self.txtStock.text())
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '시작일자', self.txtDate.text())

        ret = self.kiwoom.dynamicCall(
            "CommRqData(QString, QString, int, QString", 
            self.rqname, 
            self.opt,
            self.isnext, 
            self.viewnum)
        
        print('ret:', ret)

        if ret != 0:
            print('ret -> self.isnext:', self.isnext)
            if self.isnext != 2:
                QtWidgets.QMessageBox.about(self, "Error", "조회 실행 실패")
            else:
                self.isnext = 0

    def ProcResult(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        '''
        '''

        if self.viewnum != screen_no or rqname != self.rqname:
            return

        if self.isnext == 0:
            self.result.clearContents()
            self.result.setRowCount(0)

        if next == '2':
            self.isnext = 2

        kiwoom = Kiwoom.getInstance()

        cnt = kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        curidx = self.result.rowCount()
        self.result.setRowCount(curidx + cnt)
        print(f'curidx:{curidx}, cnt:{cnt}')

        for i in range(cnt):
            for c, column in enumerate(self.columns):
                item = kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString", trcode, '', rqname, i, column).strip()
                self.result.setItem(i+curidx, c, QtWidgets.QTableWidgetItem(item))

        print('self.isnext:', self.isnext)
        if self.isnext:
            self.ProcOpenApi()

if __name__ == '__main__':
    import sys
    from MainForm import MainForm
    app = QtWidgets.QApplication(sys.argv)
    mainform = MainForm()
    mainform.show()

    app.exec_()
    print('after event loop')
    form = DayTradingDetailForm('0000')
