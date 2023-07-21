from enum import Enum


class Choices(Enum):
    """
    Допустимые параметры для аргумента --output.
    См. модуль configs.py.
    configure_argument_parser.parser.add_argument()
    * pretty - вывод в табличной форме прямо в консоль
    * file - загрузка данных в виде файла архива
    """
    PRETTY = 'pretty'
    FILE = 'file'

    def __str__(self):
        return self.value
