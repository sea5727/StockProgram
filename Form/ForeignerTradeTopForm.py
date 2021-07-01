import sys
sys.path.append("..")

from PyQt5 import QtWidgets
from kiwoom import Kiwoom
from ObserverImpl import OnRecieveTrDataEventObserver
from matplotlib import pyplot as plt
from Entity import Entity
from datetime import datetime

plt.rcParams["font.family"] = 'Malgun Gothic' 

class ForeignerTradeTopForm(QtWidgets.QDialog, OnRecieveTrDataEventObserver):
    def __init__(self, viewnum):
        '''
        '''
        super().__init__()

        self.viewnum = viewnum
        self.rqname = '외국인기관매매상위요청'
        self.opt = 'OPT90009'

        self.isnext = 0

        self.setWindowTitle(self.rqname)
        self.resize(600, 600)
        
        self.targets = [('_', '외인순매도'), ('_', '외인순매수'), ('_', '기관순매도'), ('_', '기관순매수')]

        self.markets = [('000', '전체'), ('001', '코스피'), ('101', '코스닥')]
        self.prices = [('1', '금액(천만)'), ('2', '수량(천)')]
        self.dates = [('0', '조회일자 미포함'), ('1', '조회일자 포함')]

        
        self.cbxTargets = QtWidgets.QComboBox()
        self.cbxTargets.addItems(Entity(self.targets))

        self.cbxMarkets = QtWidgets.QComboBox()
        self.cbxMarkets.addItems(Entity(self.markets))

        self.cbxPriceOrNumber = QtWidgets.QComboBox()
        self.cbxPriceOrNumber.addItems(Entity(self.prices))

        self.cbxDates = QtWidgets.QComboBox()
        self.cbxDates.addItems(Entity(self.dates))

        self.txtDate = QtWidgets.QLineEdit()
        now = datetime.now()
        self.txtDate.setText(now.strftime('%Y%m%d'))
        
        self.btnSearch = QtWidgets.QPushButton()
        self.btnSearch.setText('조회')
        self.btnSearch.clicked.connect(self.on_clicked_btnSearch)


        columns = ["종목코드", "종목명", "금액(천만)", "수량"]
        self.result = QtWidgets.QTableWidget()
        self.result.setColumnCount(len(columns))
        self.result.setHorizontalHeaderLabels(columns)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.layout.addWidget(self.cbxTargets)
        self.layout.addWidget(self.cbxMarkets)
        self.layout.addWidget(self.cbxPriceOrNumber)
        self.layout.addWidget(self.cbxDates)
        self.layout.addWidget(self.txtDate)

        self.layout.addWidget(self.btnSearch)
        self.layout.addWidget(self.result)
        self.setLayout(self.layout)

        Kiwoom.getInstance().obs.AddObserver(self)

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

        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '시장구분', self.markets[self.cbxMarkets.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '금액수량구분', self.prices[self.cbxPriceOrNumber.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '조회일자구분', self.dates[self.cbxDates.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '날짜', self.txtDate.text())

        ret = self.kiwoom.dynamicCall(
            "CommRqData(QString, QString, int, QString", 
            self.rqname, 
            self.opt,
            self.isnext, 
            self.viewnum)

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

        names = []
        scores = []

        for i in range(cnt):

            
            prefix = self.cbxTargets.currentText()
            
            code = kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString", trcode, '', rqname, i, f'{prefix}종목코드').strip()
            name = kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString", trcode, '', rqname, i, f'{prefix}종목명').strip()
            price = kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString", trcode, '', rqname, i, f'{prefix}금액').strip()
            count = kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString", trcode, '', rqname, i, f'{prefix}수량').strip()
            _ = kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString", trcode, '', rqname, i, '대칭구분').strip()

            names.append(name[:5] if len(name) > 5 else name)
            scores.append(price)


            self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(code))
            self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(name))
            self.result.setItem(i, 2, QtWidgets.QTableWidgetItem(price))
            self.result.setItem(i, 3, QtWidgets.QTableWidgetItem(count))

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
    form = ForeignerTradeTopForm('0000')
