
from abc import ABC, abstractmethod

class GitObject(ABC):
    def __init__(self, data=None):
        if data:
            self.deserialize(data)
        else:
            self.init()
    @abstractmethod
    def serialize(self, data):
        pass
    @abstractmethod
    def deserialize(self, data):
        pass
    @abstractmethod
    def init(self):
        pass

