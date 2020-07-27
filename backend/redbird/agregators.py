from abc import (
    ABC,
    abstractmethod)
import json

from typing import List, Any, Dict

from yellowbird.models import User, Department
from bluebird.models import Contragent, DocumentsPackage


class Parameter:
    """
    param_type must be one of JSON types.
    _______________
    | JSON |Python|
    ===============
    |object| dict |
    ---------------
    | array| list |
    ---------------
    |string|  str |
    ---------------
    |  int |  int |
    ---------------
    | real |float |
    ---------------
    | true | True |
    ---------------
    | false|False |
    ---------------
    | null | None |
    ---------------
    """
    SERIALIZE_DICT = {
        'object': dict,
        'array': list,
        'string': str,
        'int': int,
        'real': float,
        'true': True,
        'false': False,
        'null': None
    }

    __parameter_name = str()
    __parameter_type = None
    description = ''

    def __init__(self, param_name: str, param_type: str,
                 description: str = ''):
        self.__parameter_name = param_name
        self.__parameter_type = param_type
        self.description = description

    @property
    def param_name(self):
        return self.__parameter_name

    @param_name.setter
    def param_name(self, val):
        pass

    @property
    def param_type(self):
        return self.__parameter_type

    @param_type.setter
    def param_type(self, val):
        pass

    def is_type(self, val):
        return self.SERIALIZE_DICT[self.param_type] == type(val)

    def __str__(self):
        return json.dumps(dict(name=self.param_name,
                               tupe=self.param_type,
                               desc=self.description))


class Agregator(ABC):
    __name = ''
    __data:  Dict[Any, Any] = dict()
    _parametries: List[Parameter] = list()

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

    def get_params(self):
        return [str(p) for p in self._parametries]

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {self.name: self.__data}

    @abstractmethod
    def calculate(self):
        raise NotImplementedError()


class JournalAgregator(Agregator):
    __name = 'journal'

    _parametries = [
        Parameter('id_list', 'array', 'List of chousen contragents.'),
        Parameter('data_from', 'string', 'Since package was created.'),
        Parameter('data_to', 'string', 'Up to date package was created.'),
    ]

    def calculate(self, params):
        """
            Пройтись по каждому контрагенту,
            по каждому пакету у контрагента,
            у каждого пакета найти журнал,
            у каждого журнала найти последние статусы
        """

        # ids = params.get('id_list', 'null')
        # data_from = params.get('data_from', '0001-1-1')
        # data_to = params.get('data_to', '9999-31-12')
        


AGREGATORS_LIST = [
    (0, None),
    (1, JournalAgregator),
]
