import sys
sys.path.append("..")

from PyQt5 import QtWidgets
from kiwoom import Kiwoom
from ObserverImpl import OnRecieveTrDataEventObserver
from matplotlib import pyplot as plt
from Entity import Entity
from datetime import datetime

plt.rcParams["font.family"] = 'Malgun Gothic' 

class TradingVolumeSoarForm(QtWidgets.QDialog, OnRecieveTrDataEventObserver):
    def __init__(self, viewnum):
        '''
        '''
        super().__init__()

        self.viewnum = viewnum
        self.rqname = '거래량급증요청'
        self.opt = 'OPT10023'

        self.isnext = 0

        self.setWindowTitle(self.rqname)
        self.resize(600, 600)
        
        self.markets = [('000', '전체'), ('001', '코스피'), ('101', '코스닥')]
        self.cond_sorts = [('1', '급증량'), ('2', '급증률')]
        self.cond_time = [('1', '분'), ('2', '전일')]
        self.cond_trading_volume = [('5', '5천주이상'), ('10', '만주이상'), ('50', '5만주이상'), ('100', '100만주이상'), ('200', '20만주이상'), ('300', '30만주이상'), ('500', '50만주이상'), ('1000', '백만주이상')]
        self.cond_stocks = [('0', '전체조회'), ('1', '관리종목제외'), ('5', '증100제외'), ('6', '증100만보기'), ('7', '증40만보기'), ('8', '증30만보기'), ('9', '증20만보기')]
        self.cond_prices = [('0', '전체조회'), ('2', '5만원이상'), ('5', '1만원이상'), ('6', '5천원이상'), ('8', '1천원이상'), ('9', '10만원이상')]


        self.cbxMarkets = QtWidgets.QComboBox()
        self.cbxMarkets.addItems(Entity(self.markets))

        self.cbxCondSorts = QtWidgets.QComboBox()
        self.cbxCondSorts.addItems(Entity(self.cond_sorts))

        self.cbxCondTime = QtWidgets.QComboBox()
        self.cbxCondTime.addItems(Entity(self.cond_time))

        self.cbxCondTradingVolume = QtWidgets.QComboBox()
        self.cbxCondTradingVolume.addItems(Entity(self.cond_trading_volume))

        self.txtTime = QtWidgets.QLineEdit()
        self.txtTime.setText('5')

        self.cbxCondStocks = QtWidgets.QComboBox()
        self.cbxCondStocks.addItems(Entity(self.cond_stocks))

        self.cbxCondPrices = QtWidgets.QComboBox()
        self.cbxCondPrices.addItems(Entity(self.cond_prices))

        self.btnSearch = QtWidgets.QPushButton()
        self.btnSearch.setText('조회')
        self.btnSearch.clicked.connect(self.on_clicked_btnSearch)

        self.result = QtWidgets.QTableWidget()
        self.columns = ['종목코드', '종목명', '현재가', '전일대비기호', '전일대비', '등락률', '이전거래량', '현재거래량', '급증량', '급증률']
        self.result.setColumnCount(len(self.columns))
        self.result.setHorizontalHeaderLabels(self.columns)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.layout.addWidget(self.cbxMarkets)
        self.layout.addWidget(self.cbxCondSorts)
        self.layout.addWidget(self.cbxCondTime)
        self.layout.addWidget(self.cbxCondTradingVolume)
        self.layout.addWidget(self.txtTime)
        self.layout.addWidget(self.cbxCondStocks)
        self.layout.addWidget(self.cbxCondPrices)

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

        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '시장구분', self.markets[self.cbxMarkets.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '정렬구분', self.cond_sorts[self.cbxCondSorts.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '시간구분', self.cond_time[self.cbxCondTime.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '거래량구분', self.cond_trading_volume[self.cbxCondTradingVolume.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '시간', self.cond_time[self.cbxCondTime.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '종목조건', self.cond_stocks[self.cbxCondStocks.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '가격구분', self.cond_prices[self.cbxCondPrices.currentIndex()][0])


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
    form = TradingVolumeSoarForm('0000')
