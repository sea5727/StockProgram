from PyQt5 import QAxContainer
from ObserverImpl import OnRecieveTrDataEventObserverImpl

class Kiwoom():
    __openapi = None
    def __init__(self):
        '''
        '''
    
    @staticmethod
    def getInstance():
        if Kiwoom.__openapi == None:
            Kiwoom.__openapi = OpenAPI()
        return Kiwoom.__openapi

class OpenAPI(QAxContainer.QAxWidget):

    def __init__(self):
        '''
        '''
        super().__init__()

        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')

        self.OnEventConnect.connect(self.onEventConnect)
        self.OnReceiveTrData.connect(self.onReceiveTrData)

        self.obs = OnRecieveTrDataEventObserverImpl()

        self.viewnum = []
        for i in range(2000):
            self.viewnum.append(str(i))

    def onEventConnect(self, err_code):
        '''
        '''
        print('onEventConnect errCode:', err_code)

    def onReceiveTrData(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        '''
        '''
        self.obs.Notify(screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4)

    def login(self):
        '''
        '''
        return self.dynamicCall('CommConnect()')
    
