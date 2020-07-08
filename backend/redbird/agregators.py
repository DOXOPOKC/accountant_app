from abc import (
    ABC,
    abstractmethod)
import json


class Agregator(ABC):
    __name = ''
    __data = {}

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {self.name: self.__data}

    @abstractmethod
    def calculate(self):
        raise NotImplementedError()


class JournalAgregator(Agregator):
    __name = 'journal'

    def calculate(self):
        """
            Пройтись по каждому контрагенту,
            по каждому пакету у контрагента,
            у каждого пакета найти журнал,
            у каждого журнала найти последние статусы
        """
        pass
