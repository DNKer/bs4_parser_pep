import csv
import datetime as dt
import logging
from typing import Dict

from prettytable import PrettyTable

from constants import (
    BASE_DIR,
    DATETIME_FORMAT,
    ENCODING,
)
from exceptions import (
    ParserDirCreateException,
    ParserFileOutputException,
)


def default_output(results, cli_args) -> None:
    """Печать списка results построчно."""
    for row in results:
        print(*row)


def pretty_output(results, cli_args) -> None:
    """Выводит данные в PrettyTable."""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args) -> None:
    """Вывод данных в файл csv."""
    results_dir = BASE_DIR / 'results'
    try:
        results_dir.mkdir(exist_ok=True)
    except OSError as error:
        logging.error(f'Ошибка создания каталога: {results_dir}. '
                      f'Ошибка: {error}')
        raise ParserDirCreateException
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    # Собираем имя файла из полученных переменных:
    # «режим работы программы» + «дата и время записи» + формат (.csv).
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    try:
        with open(file_path, 'w', encoding=ENCODING) as file:
            writer = csv.writer(file, dialect='unix')
            writer.writerows(results)
        logging.info(f'Файл с результатами был сохранён: {file_path}')
    except Exception as error:
        logging.exception(f'В процессе загрузки возникла ошибка: {error}')
        raise ParserFileOutputException


def control_output(results, cli_args) -> None:
    """Вывод в заданном формате."""
    CLI_ARGS_DICT: Dict[str, None] = {
        'pretty': pretty_output,
        'file': file_output,
        None: default_output
    }
    CLI_ARGS_DICT.get(cli_args.output)(results, cli_args)
