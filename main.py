# 28 вариант
import argparse
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
        _data : list
            Список словарей, в котором будут хранится записи из файла
    '''
    _data: list

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
            Список словарей, в котором будут хранится записи из файла
        __error : dictionary
            Словарь, в котором хранится статистика невалидных записей
        __valid : list
            Список словарей, в котором хранятся валидные записи
    '''
    __collection: list
    __error: dict
    __valid: list
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
        self.__valid = []
        self.__error = {
                        'length': 0,
                        'telephone': 0,
                        'height': 0,
                        'character': 0,
                        'separator': 0,
                        'address': 0,
                        'academic_degree': 0,
                        'worldview': 0
                        }

    @property
    def collection(self) -> list:
        '''
        Коллекция экземпляров класса записей в качества свойства класса validator.

        Returns
        -------
          list:
            Возвращается список словарей с записями.
        '''
        return self.__collection
    @property
    def valid(self) -> list:
        '''
        Получение валидных записей.

        Returns
        -------
          dict:
            Возвращается словарь с валидными записями.
        '''
        return self.__valid

    def check_length(self, number: str or int, flag: str) -> bool:
        '''
        Выполняет проверку корректности длины номера/серии паспорта/СНИЛС.

        Если длина номера/серии паспорта/СНИЛС не соответсвует формату,
        то будет возвращено False.

        Parameters
        ----------
            number : str or int
                Строка с проверяемым номером.
                Или проверяемое число (серия паспорта/СНИЛС)
            flag : str
                Строка с видом парметра (номер/серия паспорта/СНИЛС).

        Returns
        -------
            bool:
                Булевый результат проверки на корректность
        '''
        reference_length = 0
        if flag == 'telephone':
            reference_length = 18
        elif flag == 'passport_number':
            reference_length = 6
        elif flag == 'snils':
            reference_length = 11
        if reference_length == len(str(number)):
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
    def check_height(self, param: str) -> bool:
        '''
        Выполняет проверку значений роста.

        Если физические параметры роста выходят за пределы разумного,
        то будет возвращено False.

        Parameters
        ----------
            param : str
                Строка со значением роста

        Returns
        -------
        bool:
            Булевый результат проверки на корректность
        '''

        if float(param) > 2.20:
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
    def check_separator(self, element: str) -> bool:
        '''
        Выполняет проверку ,что разделитель вещественного числа ".".

        Если разделитель вещественного числа отличен от ".",
        то будет возвращено False.

        Parameters
        ----------
            element : str
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

    def check_academic_degree(self, academic_degree: str) -> bool:
        '''
        Выполняет проверку academic_degree на корректность.

        Если academic_degree не входит в список "правильных" academic_degree,
        то будет возвращено False.

        Parameters
        ----------
            academic_degree : str
                Строка с проверяемым academic_degree

        Returns
        -------
        bool:
        Булевый результат проверки на корректность
        '''
        correct_academic_degree = ['Бакалавр', 'Магистр', 'Доктор наук', 'Кандидат наук', 'Специалист']
        if academic_degree in correct_academic_degree:
            return True
        return False
    def check_worldview(self, worldview: str) -> bool:
        '''
        Выполняет проверку academic_degree на корректность.

        Если academic_degree не входит в список "правильных" academic_degree,
        то будет возвращено False.

        Parameters
        ----------
            worldview : str
                Строка с проверяемым academic_degree

        Returns
        -------
        bool:
        Булевый результат проверки на корректность
        '''
        correct_worldview = ['Буддизм', 'Конфуцианство', 'Деизм', 'Секулярный гуманизм', 'Агностицизм', 'Иудаизм',
                             'Атеизм', 'Католицизм', 'Пантеизм']
        if worldview in correct_worldview:
            return True
        return False

    def valid_function(self) -> None:
        '''
        Выполняет проверку валидности записей.

        Если запись валидна,то записывается в __valid.

        Parameters
        ----------

        Returns
        -------
            None:
                Ничего не возвращает
        '''
        for i in self.__collection and tqdm(self.__collection, colour='green'):
            if (self.check_length(i['telephone'], 'telephone') == False or
                    self.check_length(i['snils'], 'snils') == False or
                    self.check_length(i['passport_number'], 'passport_number') == False):
                self.__error['length'] += 1
                continue
            elif self.check_academic_degree(i['academic_degree']) == False:
                self.__error['academic_degree'] += 1
                continue
            elif self.check_worldview(i['worldview']) == False:
                self.__error['worldview'] += 1
                continue
            elif self.check_telephone(i['telephone']) == False:
                 self.__error['telephone'] += 1
                 continue
            elif self.check_separator(i['height']) == False:
                self.__error['separator'] += 1
                continue
            elif self.check_height(i['height']) == False:
                self.__error['height'] += 1
                continue
            elif (self.check_character(i['snils']) == False or
                    self.check_character(i['passport_number']) == False or
                    self.check_character(i['age']) == False):
                self.__error['character'] += 1
                continue
            elif self.check_address(i['address']) == False:
                self.__error['address'] += 1
                continue
            else:
                self.__valid.append(i)

    def write_in_new_file(self) -> None:
        '''
        Создает новый файл, в который записывает валидные данные.

        Parameters
        ----------

        Returns
        -------
            None:
                Не возвращает ничего
        '''
        with open('new_28.txt', mode='w', encoding='windows-1251') as f:
            f.write(json.dumps(self.valid))

    def statistics(self) -> None:
        '''
            Выводит статистику обработанных записей.

            Parameters
            ----------

            Returns
            -------
                None:
                    Не возвращает ничего
            '''
        print('Число валидных записей {}'. format(len(self.__valid)))
        print('Число невалидных записей {}'.format(len(self.__collection) - len(self.__valid)))
        print('Ошибки')
        print(json.dumps(self.__error, indent=4))


# w_dict = []
# for i in B.collection:
#     w_dict.append(i['worldview'])
# print(w_dict)
#
# counts = {}
# for i in w_dict:
#     if i not in counts:
#         counts[i] = 0
#     counts[i] += 1
# print(counts)



B = validator(r'/Users/dary/PycharmProjects/прикладное_программирование_лаба2/28.txt')
print(B.collection[0])


B.valid_function()
# print(B.valid[0:5])
B.statistics()
# B.write_in_new_file()

# parser = argparse.ArgumentParser()
# parser.add_argument('input', default='input.txt')
# parser.add_argument('output', default='output.txt')
# namespace = parser.parse_args()
# inputPath = namespace.input
# outputPath = namespace.output
# print(inputPath)
# print(outputPath)
