# 28 вариант
import os
import re
import json
import time
from tqdm import tqdm

class to_write_from:
    '''
      Объект класса to_write_from читает данные с файла.

      Он нужен для того, чтобы считать и записать данные с/в файл(а).

      Attributes
      ----------
        _data : dictionary
            Словарь, в котором будут хранится записи из файла
      '''
    _data: dict

    def __init__(self, path: str) -> None:
        '''
            Инициализирует экземпляр класса to_write_from.

            Parameters
            ----------
              path : str
                Строковый параметр: путь до открываемого файла
            '''
        self._data = json.load(open(path, encoding='windows-1251'))

#класс для валидатора
class validator(to_write_from):
    '''
          Объект класса validator производит валидацию данных.

          Он нужен для того, чтобы произвести валидацию записей исходного файла,
          сохранить релевантные записи в новый файл. Также собирает статистику
          по числу невалидных записей и типам ошибок.
          Данный класс validator отнаследован от класса to_write_from.

          Attributes
          ----------
            __collection : dictionary
            Словарь, в котором будут хранится записи из файла
            __error : dictionary
            Словарь, в котором хранится статистика невалидных записей
            __valid : dictionary
            Словарь, в котором хранятся валидные записи

          '''
    __collection: dict
    __error: dict
    __valid: dict
    def __init__(self, path: str) -> None:
        '''
            Инициализирует экземпляр класса validator.

            Parameters
            ----------
              path : str
                Строковый параметр: путь до открываемого файла
            '''
        to_write_from.__init__(self, path)
        self.__collection = self._data
        #self.__valid = open('valid.txt', mode='a+')
        self.__error = {
                        'length': 0,
                        'telephone': 0,
                        'height': 0,
                        'character': 0,
                        'inappropriate': 0,
                        'separator': 0,
                        'address': 0,
                        }

    @property
    def collection(self) -> dict:
        '''
        Коллекция экземпляров класса записей в качества свойства класса validator.

        Returns
        -------
          dict:
            Возвращается словарь с записями.
        '''
        return self.__collection

    def check_length(self, number: str, flag: str) -> bool:
        '''
                  Выполняет проверку корректности длины номера/серии паспорта/СНИЛС.

                  Если длина номера/серии паспорта/СНИЛС не соответсвует формату,
                  то будет возвращено False.

                  Parameters
                  ----------
                    number : str
                      Строка с проверяемым номером/серией паспорта/СНИЛСом
                    flag : str
                      Строка с видом парметра (номер/серия паспорта/СНИЛС).

                  Returns
                  -------
                    bool:
                      Булевый результат проверки на корректность
                  '''
        reference_length = 0
        if flag == 'номер':
            reference_length = 18
        elif flag == 'паспорт':
            reference_length = 6
        elif flag == 'снилс':
            reference_length = 11
        if reference_length == len(number):
            return True
        return False
    def check_telephone(self, telephone: str) -> bool:
        '''
        Выполняет проверку корректности телефонного номера.

        Если строка не соответсвует шаблону, то будет возвращено False.

        Parameters
        ----------
          telephone : str
            Строка с проверяемым телефонным номером

        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''
        pattern = "^((\+?7|8)[\-])((\(\d{3}\))|(\d{3}))([\-])(\d{3}[\-]\d{2}[\-]\d{2})$"
        if re.match(pattern, telephone):
            return True
        return False
    def check_height(self, param: float) -> bool:
        '''
                  Выполняет проверку значений роста.

                  Если физические параметры роста выходят за пределы разумного,
                  то будет возвращено False.

                  Parameters
                  ----------
                    param : float
                      Строка со значением роста

                  Returns
                  -------
                    bool:
                      Булевый результат проверки на корректность
                  '''

        if param > 2.20:
            return False
        return True
    def check_character(self, number: int) -> bool:
        '''
                  Проверяет наличие символа в числовых данных.

                  Если в числовых данных встречается символ,
                  то будет возвращено False.

                  Parameters
                  ----------
                    number : int
                      Проверяемые числовые данные

                  Returns
                  -------
                    bool:
                      Булевый результат проверки на корректность
                  '''
        return str(number).isdigit()
    def check_inappropriate(self, information: str, flag: str) -> bool:## todo
        '''
                  Проверяет корректность данных в графе профессия, звание, религия.

                  Если в графе профессия, звание, религия указаны неподходящие данные,
                  то будет возвращено False.

                  Parameters
                  ----------
                    information : str
                      Строка с проверяемым параметром
                      flag : str
                      Строка с видом парметра (профессия/звание/религия)

                  Returns
                  -------
                    bool:
                      Булевый результат проверки на корректность
                  '''
        if flag == 'профессия':
            information = 18
        elif flag == 'звание':
            information = 6
        elif flag == 'религия':
            information = 11
        if reference_length == len(number):
            return True
        return False
    def check_separator(self, element: float) -> bool:
        '''
                  Выполняет проверку ,что разделитель вещественного числа ".".

                  Если разделитель вещественного числа отличен от ".",
                  то будет возвращено False.

                  Parameters
                  ----------
                    element : float
                      Проверяемое число

                  Returns
                  -------
                    bool:
                      Булевый результат проверки на корректность
                  '''
        if re.match(r'^-?\d+(?:\.\d+)$', str(element)) is None:
            return False
        return True
    def check_address(self, address: str) -> bool:
        '''
                  Выполняет проверку формата адреса.

                  Если адрес проживания указан не в формате "улица пробел номер дома",
                  то будет возвращено False.

                  Parameters
                  ----------
                    address : str
                      Строка с проверяемым адресом

                  Returns
                  -------
                    bool:
                      Булевый результат проверки на корректность
                  '''
        pattern = "^[А-Яа-я]([А-Яа-я]+\s)+\d{1,4}$"
        if re.match(pattern, address):
            return True
        return False

        



# A = to_write_from(r'/Users/dary/PycharmProjects/прикладное_программирование_лаба2/28.txt')
# print(A._data[0:2])

B = validator(r'/Users/dary/PycharmProjects/прикладное_программирование_лаба2/28.txt')
print(B.collection[0])

# print(B.check_length(B.collection[0]['snils'], 'снилс'))
print(B.check_separator(B.collection[0]['age']))
