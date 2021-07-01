import sys
sys.path.append("..")

from PyQt5 import QtWidgets
from kiwoom import Kiwoom
from ObserverImpl import OnRecieveTrDataEventObserver
from matplotlib import pyplot as plt
from Entity import Entity
from datetime import datetime

plt.rcParams["font.family"] = 'Malgun Gothic' 

class MarketTopPerInvestorForm(QtWidgets.QDialog, OnRecieveTrDataEventObserver):
    def __init__(self, viewnum):
        '''
        '''
        super().__init__()

        self.viewnum = viewnum
        self.rqname = '장중투자자별매매상위'
        self.opt = 'OPT10065'

        self.isnext = 0

        self.setWindowTitle(self.rqname)
        self.resize(600, 600)
        
        self.cond_trading = [('1', '순매수'), ('2', '순매도')]
        self.cond_markets = [('000', '전체'), ('001', '코스피'), ('101', '코스닥')]
        self.cond_institution = [('9000', '외국인'), ('9100', '외국계'), ('1000', '금융투자'), ('3000', '투신'), ('5000', '기타금융'), ('4000', '은행'), ('2000', '보험'), ('6000', '연기금'), ('7000', '국가'), ('7100', '기타법인'), ('9999', '기관계')]

        self.cbxCondTrading = QtWidgets.QComboBox()
        self.cbxCondTrading.addItems(Entity(self.cond_trading))

        self.cbxCondMarkets = QtWidgets.QComboBox()
        self.cbxCondMarkets.addItems(Entity(self.cond_markets))

        self.cbxCondInstitution = QtWidgets.QComboBox()
        self.cbxCondInstitution.addItems(Entity(self.cond_institution))

        self.btnSearch = QtWidgets.QPushButton()
        self.btnSearch.setText('조회')
        self.btnSearch.clicked.connect(self.on_clicked_btnSearch)

        self.result = QtWidgets.QTableWidget()
        self.columns = ['종목코드', '종목명', '매도량', '매수량', '순매도']
        self.result.setColumnCount(len(self.columns))
        self.result.setHorizontalHeaderLabels(self.columns)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.layout.addWidget(self.cbxCondTrading)
        self.layout.addWidget(self.cbxCondMarkets)
        self.layout.addWidget(self.cbxCondInstitution)

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

        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '매매구분', self.cond_trading[self.cbxCondTrading.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '시장구분', self.cond_markets[self.cbxCondMarkets.currentIndex()][0])
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '기관구분', self.cond_institution[self.cbxCondInstitution.currentIndex()][0])

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
    form = MarketTopPerInvestorForm('0000')
