from abc import ABCMeta, abstractmethod

class OnRecieveTrDataEventObserver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def OnNotify(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        pass


class OnRecieveTrDataEventObserverImpl:
    
    def __init__(self):
        self.__observer_list = []

    def AddObserver(self, o):
        self.__observer_list.append(o)

    def DelObserver(self, o):
        self.__observer_list.remove(o)

    def Notify(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        for o in self.__observer_list:
            o.OnNotify(screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4)




# class Subject:
#     __metaclass__ = ABCMeta

#     @abstractmethod
#     def AddObserver(self):
#         pass

#     @abstractmethod
#     def DelObserver(self):
#         pass

#     @abstractmethod
#     def Notify(self):
#         pass

# class Observer:

#     @abstractmethod
#     def update(self, temperature, humidity, pressure):
#         pass

#     @abstractmethod
#     def register_subject(self, subject):
#         pass


# class weejiwon(Subject):
#     def __init__(self):
#         super(weejiwon, self).__init__()
#         self._observer_list = []
#         self.happiness = 0
#         self.sadness = 0

#     def AddObserver(self, observer):
#         if observer in self._observer_list:
#             return "Already exist observer!"
        
#         self._observer_list.append(observer)
#         return "Success register!"

#     def DelObserver(self, observer):
#         if observer in self._observer_list:
#             self._observer_list.remove(observer)
#             return "Success remove!"

#         return "observer does not exist."

#     def Notify(self): #옵저버에게 알리는 부분 (옵저버리스트에 있는 모든 옵저버들의 업데이트 메서드 실행)
#         for observer in self._observer_list:
#             observer.update(self.happiness,self.sadness)

#     def emotionalChanged(self):
#         self.Notify() #감정이 변하면 옵저버에게 알립니다.

#     def set_emotional(self, happiness,sadness):
#         self.happiness=happiness
#         self.sadness=sadness
#         self.emotionalChanged()

# class Emotion(Observer):
#     def update(self, happiness,sadness): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
#         self.happiness=happiness
#         self.sadness=sadness
#         self.display()

#     def register_subject(self, subject):
#         self.subject = subject
#         self.subject.AddObserver(self)

#     def display(self):
#         print ('weejiwon Emotion happiness:',self.happiness,' sadness:',self.sadness)

# def test():
#     weejiwonObj = weejiwon()
#     EmotionObj=Emotion()
#     EmotionObj.register_subject(weejiwonObj)


#     weejiwonObj.set_emotional('good','good')
#     weejiwonObj.set_emotional('Not good','Not good')
#     weejiwonObj.set_emotional('Bad','Bad')

# if __name__ == '__main__':
#     test()
