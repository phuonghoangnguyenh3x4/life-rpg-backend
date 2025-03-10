from abc import ABC, abstractmethod

class Task(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def execute(self, context):
        pass 
