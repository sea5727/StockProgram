import sys
sys.path.append("..")

from PyQt5 import QtWidgets
from kiwoom import Kiwoom
from ObserverImpl import OnRecieveTrDataEventObserver
from matplotlib import pyplot as plt
from Entity import Entity
from datetime import datetime, timedelta
import pandas as pd
import mplfinance as fplt
import numpy as np

import plotly.graph_objects as go

plt.rcParams["font.family"] = 'Malgun Gothic' 

class StockDayCandleChartForm(QtWidgets.QDialog, OnRecieveTrDataEventObserver):
    def __init__(self, viewnum):
        '''
        '''
        super().__init__()

        self.viewnum = viewnum
        self.rqname = '주식일봉차트조회요청'
        self.opt = 'OPT10081'

        self.isnext = 0

        self.setWindowTitle(self.rqname)
        self.resize(600, 600)
        
        self.cond_price = [('0', '수신데이터'), ('1', '유상증자'), ('2', '무상증자'), ('4', '배당락'), ('8', '액멸분할'), ('16', '액면병합'), ('32', '기업합병'), ('64', '감자'), ('256', '권리락')]

        self.txtStock = QtWidgets.QLineEdit()
        self.txtStock.setText('005930')

        self.txtDate = QtWidgets.QLineEdit()
        self.txtDate.setText(datetime.now().strftime('%Y%m%d'))

        self.cbxCondPrice = QtWidgets.QComboBox()
        self.cbxCondPrice.addItems(Entity(self.cond_price))

        self.btnSearch = QtWidgets.QPushButton()
        self.btnSearch.setText('조회')
        self.btnSearch.clicked.connect(self.on_clicked_btnSearch)

        self.result = QtWidgets.QTableWidget()
        self.columns = ['종목코드', '일자', '현재가', '거래량', '거래대금', '시가', '고가', '저가']
        
        self.result.setColumnCount(len(self.columns))
        self.result.setHorizontalHeaderLabels(self.columns)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.layout.addWidget(self.txtStock)
        self.layout.addWidget(self.txtDate)
        self.layout.addWidget(self.cbxCondPrice)


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
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '기준일자', self.txtDate.text())
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '수정주가구분', self.cond_price[self.cbxCondPrice.currentIndex()][0])

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


        dates = []
        opens = []
        closes = []
        highes = [] 
        lowes = []
        volumes = []

        item = None
        now = datetime.now()
        for i in range(cnt):
            for c, column in enumerate(self.columns):

                item = kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString", trcode, '', rqname, i, column).strip()
                if column == '일자':
                    date = datetime.strptime(item, '%Y%m%d')
                    # if now - timedelta(weeks=4) >= date:
                    #     break
                    dates.append(item)
                elif column == '시가':
                    opens.append(item)
                elif column == '현재가':
                    closes.append(item)
                elif column == '고가':
                    highes.append(item)
                elif column == '저가':
                    lowes.append(item)
                elif column == '거래량':
                    volumes.append(item)

                self.result.setItem(i+curidx, c, QtWidgets.QTableWidgetItem(item))


        dataframe = {
            'Open': map(np.int64, opens),
            'High': map(np.int64, highes),
            'Low': map(np.int64, lowes),
            'Close': map(np.int64, closes),
            'Volume': map(np.int64, volumes),
        }

        df = pd.DataFrame(dataframe, pd.to_datetime(dates))[:60]
        df = df.reindex(index=df.index[::-1])

        from Expression import testfunc

        testfunc.func1(df)


        colorset = fplt.make_marketcolors(up='tab:red', down='tab:blue', volume='tab:blue')
        s = fplt.make_mpf_style(marketcolors=colorset)
        fplt.plot(df, type='candle', volume=True, style=s, mav=(5, 10, 20, 60))

        return
        # if self.isnext:
        #     self.ProcOpenApi()

if __name__ == '__main__':
    import sys
    from MainForm import MainForm
    app = QtWidgets.QApplication(sys.argv)
    mainform = MainForm()
    mainform.show()

    app.exec_()
    print('after event loop')
    form = StockDayCandleChartForm('0000')
