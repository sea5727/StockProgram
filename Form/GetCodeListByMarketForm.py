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

class GetCodeListByMarketForm(QtWidgets.QDialog, OnRecieveTrDataEventObserver):
    def __init__(self, viewnum):
        '''
        '''
        super().__init__()

        self.viewnum = viewnum
        self.rqname = '종목코드조회요청'
        self.opt = 'OPT10081'

        self.isnext = 0

        self.setWindowTitle(self.rqname)
        self.resize(600, 600)
        
        self.cond_markets = [('0', '코스피'), ('10', '코스닥'), ('3', 'ELW'), ('8', 'ETF'), ('50', 'KONEX'), ('4', '뮤추얼펀드'), ('5', '신주인수권'), ('6', '리츠'), ('9', '하이얼펀드'), ('30', 'K-OTC')]
        self.cbxCondMarkets = QtWidgets.QComboBox()
        self.cbxCondMarkets.addItems(Entity(self.cond_markets))

        self.btnSearch = QtWidgets.QPushButton()
        self.btnSearch.setText('조회')
        self.btnSearch.clicked.connect(self.on_clicked_btnSearch)

        # self.result = QtWidgets.QTableWidget()
        # self.columns = ['종목코드', '일자', '현재가', '거래량', '거래대금', '시가', '고가', '저가']
        
        # self.result.setColumnCount(len(self.columns))
        # self.result.setHorizontalHeaderLabels(self.columns)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.layout.addWidget(self.cbxCondMarkets)

        self.layout.addWidget(self.btnSearch)
        # self.layout.addWidget(self.result)
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

        selected_value = self.cond_markets[self.cbxCondMarkets.currentIndex()][0]
        selected_name = self.cond_markets[self.cbxCondMarkets.currentIndex()][1]

        code_list = self.kiwoom.dynamicCall('GetCodeListByMarket(QString)', selected_value)
        code_list = code_list.split(';')[:-1]

        print(f'{selected_name} 시장 개수 : {len(code_list)}')
        
        # for idx, code in enumerate(code_list):
        #     self.kiwoom.dynamicCall('DisconnectRealData(QString)', )
        


    def ProcResult(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        '''
        '''
        print('ProcResult')

if __name__ == '__main__':
    import sys
    from MainForm import MainForm
    app = QtWidgets.QApplication(sys.argv)
    mainform = MainForm()
    mainform.show()

    app.exec_()
    print('after event loop')
    form = GetCodeListByMarketForm('0000')
