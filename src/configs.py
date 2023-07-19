import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import (
    BACKUP_COUNT,
    DATETIME_FORMAT,
    LOG_DIR,
    LOG_FILE,
    LOG_FORMAT,
    MAX_BYTES
)


def configure_argument_parser(available_modes) -> argparse.ArgumentParser:
    """Допустимые аргументы парсера."""
    parser = argparse.ArgumentParser(description='Парсер документации Python')
    parser.add_argument(
        'mode',
        choices=available_modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=('pretty', 'file'),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging() -> None:
    """Конфигурация логов."""
    try:
        LOG_DIR.mkdir(exist_ok=True)
        rotating_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT
        )
        logging.basicConfig(
            datefmt=DATETIME_FORMAT,
            format=LOG_FORMAT,
            level=logging.INFO,
            handlers=(rotating_handler, logging.StreamHandler())
        )
    except OSError as error:
        logging.exception(f'В процессе создания {LOG_DIR} '
                          f'возникла ошибка: {error}')
