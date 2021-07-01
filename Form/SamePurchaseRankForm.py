import sys
sys.path.append("..")

from PyQt5 import QtWidgets
from kiwoom import Kiwoom
from ObserverImpl import OnRecieveTrDataEventObserver
from matplotlib import pyplot as plt
from Entity import Entity
from datetime import datetime

plt.rcParams["font.family"] = 'Malgun Gothic' 

class SamePurchaseRankForm(QtWidgets.QDialog, OnRecieveTrDataEventObserver):
    def __init__(self, viewnum):
        '''
        '''
        super().__init__()

        self.viewnum = viewnum
        self.rqname = '동일순매매순위요청'
        self.opt = 'opt10062'

        self.isnext = 0

        self.setWindowTitle(self.rqname)
        self.resize(600, 600)
        
        self.cond_start_date = datetime.now().strftime('%Y%m%d')
        self.cond_end_date = datetime.now().strftime('%Y%m%d')
        self.cond_markets = [('000', '전체'), ('001', '코스피'), ('101', '코스닥')]
        self.cond_trading = [('1', '순매수'), ('2', '순매도')]
        self.cond_sort = [('1', '수량'), ('2', '금액')]
        self.cond_unit = [('1', '단주', ('1000', '천주'))]


        self.txtStartDate = QtWidgets.QLineEdit()
        self.txtStartDate.setText(self.cond_start_date)

        self.txtEndDate = QtWidgets.QLineEdit()
        self.txtEndDate.setText(self.cond_start_date)

        self.cbxCondMarkets = QtWidgets.QComboBox()
        self.cbxCondMarkets.addItems(Entity(self.cond_markets))

        self.cbxCondTraing = QtWidgets.QComboBox()
        self.cbxCondTraing.addItems(Entity(self.cond_trading))

        self.cbxCondSort = QtWidgets.QComboBox()
        self.cbxCondSort.addItems(Entity(self.cond_sort))

        self.cbxCondUnit = QtWidgets.QComboBox()
        self.cbxCondUnit.addItems(Entity(self.cond_unit))

        self.btnSearch = QtWidgets.QPushButton()
        self.btnSearch.setText('조회')
        self.btnSearch.clicked.connect(self.on_clicked_btnSearch)

        self.result = QtWidgets.QTableWidget()
        self.columns = ['종목코드', '순위', '종목명', '현재가', '대비기호', '전일대비', '등락률', '누적거래량', '기관순매매수량', '기관순매매금액', '기관순매매평균가', '외인순매매수량', '외인순매매평균가', '순매매수량', '순매매금액']
        self.result.setColumnCount(len(self.columns))
        self.result.setHorizontalHeaderLabels(self.columns)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.layout.addWidget(self.txtStartDate)
        self.layout.addWidget(self.txtEndDate)
        self.layout.addWidget(self.cbxCondMarkets)
        self.layout.addWidget(self.cbxCondSort)
        self.layout.addWidget(self.cbxCondUnit)
        self.layout.addWidget(self.btnSearch)

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

        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '시작일자', self.txtStartDate.text())
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '종료일자', self.txtEndDate.text())
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '시장구분', self.cond_markets[self.cbxCondMarkets.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '매매구분', self.cond_trading[self.cbxCondTraing.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '정렬조건', self.cond_sort[self.cbxCondSort.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '단위구분', self.cond_unit[self.cbxCondUnit.currentIndex()][0])

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
    form = SamePurchaseRankForm('0000')
