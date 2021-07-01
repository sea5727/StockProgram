
from PyQt5 import QtWidgets
from kiwoom import Kiwoom
from ObserverImpl import OnRecieveTrDataEventObserver
from matplotlib import pyplot as plt
from Entity import Entity
from datetime import datetime

plt.rcParams["font.family"] = 'Malgun Gothic' 

class NewHighLowForm(QtWidgets.QDialog, OnRecieveTrDataEventObserver):
    def __init__(self, viewnum):
        '''
        '''
        super().__init__()

        self.viewnum = viewnum
        self.rqname = '신고저가요청'
        self.opt = 'OPT10016'

        self.isnext = 0

        self.setWindowTitle(self.rqname)
        self.resize(600, 600)
        
        self.markets = [('000', '전체'), ('001', '코스피'), ('101', '코스닥')]
        self.new_high_low = [('1', '신고가'), ('2', '신저가')]
        self.high_low = [('1', '고저기준'), ('2', '종가기준')]
        self.condition_stocks = [('0', '전체조회'), ('1', '관리종목제외'), ('3', '우선주제외'), ('5', '증100제외'), ('6', '증100만보기'), ('7', '증40만보기'), ('8', '증30만보기')]
        self.trading_volume = [('00000', '전체조회'), ('00010', '만주이상'), ('00050', '5만주이상'), ('00100', '10만주이상'), ('00150', '15만주이상'), ('00200', '20만주이상'), ('00300', '30만주이상'), ('00500', '50만주이상'), ('01000', '백만주이상')]
        self.credit = [('0', '전체조회'), ('1', '신용융자A군'), ('2', '신용융자B군'), ('3', '신용융자C군'), ('4', '신용융자D군'), ('5', '신용융자전체')]
        self.cap = [('0', '미포함'), ('1', '포함')]
        self.during = [('5', '5일'), ('10', '10일'), ('20', '20일'), ('60', '60일'), ('250', '250일')]


        self.cbxMarkets = QtWidgets.QComboBox()
        self.cbxMarkets.addItems(Entity(self.markets))

        self.cbxNewHighLow = QtWidgets.QComboBox()
        self.cbxNewHighLow.addItems(Entity(self.new_high_low))

        self.cbxHighLow = QtWidgets.QComboBox()
        self.cbxHighLow.addItems(Entity(self.high_low))

        self.cbxConditionStocks = QtWidgets.QComboBox()
        self.cbxConditionStocks.addItems(Entity(self.condition_stocks))

        self.cbxTradingVolume = QtWidgets.QComboBox()
        self.cbxTradingVolume.addItems(Entity(self.trading_volume))

        self.cbxCredit = QtWidgets.QComboBox()
        self.cbxCredit.addItems(Entity(self.credit))

        self.cbxCap = QtWidgets.QComboBox()
        self.cbxCap.addItems(Entity(self.cap))

        self.cbxDuring = QtWidgets.QComboBox()
        self.cbxDuring.addItems(Entity(self.during))

        self.btnSearch = QtWidgets.QPushButton()
        self.btnSearch.setText('조회')
        self.btnSearch.clicked.connect(self.on_clicked_btnSearch)

        self.result = QtWidgets.QTableWidget()
        self.columns = ['종목코드', '종목명', '현재가', '전일대비기호', '전일대비', '등락률', '거래량', '전일거래량대비율', '매도호가', '고가', '저가']
        self.result.setColumnCount(len(self.columns))
        self.result.setHorizontalHeaderLabels(self.columns)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.layout.addWidget(self.cbxMarkets)
        self.layout.addWidget(self.cbxNewHighLow)
        self.layout.addWidget(self.cbxHighLow)
        self.layout.addWidget(self.cbxConditionStocks)
        self.layout.addWidget(self.cbxTradingVolume)
        self.layout.addWidget(self.cbxCredit)
        self.layout.addWidget(self.cbxCap)
        self.layout.addWidget(self.cbxDuring)


        self.layout.addWidget(self.btnSearch)
        self.layout.addWidget(self.result)
        self.setLayout(self.layout)

        Kiwoom.getInstance().obs.AddObserver(self)
    


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
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '신고저구분', self.new_high_low[self.cbxNewHighLow.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '고저종구분', self.high_low[self.cbxHighLow.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '종목조건', self.condition_stocks[self.cbxConditionStocks.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '거래량구분', self.trading_volume[self.cbxTradingVolume.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '신용조건', self.credit[self.cbxCredit.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '상하한포함', self.cap[self.cbxCap.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '기간', self.during[self.cbxDuring.currentIndex()][0])


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
        print(f'curidx:{curidx}, cnt:{cnt}')
        self.result.setRowCount(curidx + cnt)

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
    form = NewHighLowForm('0000')
