from pathlib import Path
from typing import Dict


MAIN_DOC_URL: str = 'https://docs.python.org/3/'
PEP_URL: str = 'https://peps.python.org/'
BASE_DIR: str = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT: str = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOG_DIR: str = BASE_DIR / 'logs'
LOG_FILE: str = LOG_DIR / 'parser.log'
MAX_BYTES: int = 10 ** 6  # максимальный объём одного файла лога (байт)
BACKUP_COUNT = 5  # максимальное количество файлов с логами
# PATTERN - шаблон для поиска версии и статуса
PATTERN: str = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
# PDF_A4_TAG - шаблон для скачивания архива
#  с документацией в формате А4
PDF_A4_TAG: str = r'.+pdf-a4\.zip$'
ENCODING: str = 'utf-8'
FUTURES: str = 'lxml'
EXPECTED_STATUS: Dict = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
