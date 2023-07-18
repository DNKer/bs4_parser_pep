# configs.py
import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import (BACKUP_COUNT, BASE_DIR,  DATETIME_FORMAT, LOG_FORMAT,
                       MAX_BYTES)


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
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'parser.log'
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT
    )
    # Настройка логирования basicConfig.
    logging.basicConfig(
        datefmt=DATETIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )