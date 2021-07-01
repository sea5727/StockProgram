

class Entity:
    def __init__(self, listparam):
        ''''''

        self.size = len(listparam)
        self.data = listparam
    
    def __iter__(self):
        self.index = 0
        return self
    
    def __next__(self):
        if self.index >= self.size:
            raise StopIteration
        data = self.data[self.index][1]
        self.index += 1
        return data

