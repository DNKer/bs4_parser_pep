import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import (
    configure_argument_parser,
    configure_logging,
)
from constants import (
    BASE_DIR,
    ENCODING,
    EXPECTED_STATUS,
    FUTURES,
    MAIN_DOC_URL,
    PATTERN,
    PDF_A4_TAG,
    PEP_URL,
)
from exceptions import (
    ParserFindTagException,
    ParserDirCreateException,
)
from outputs import control_output
from utils import get_response, find_tag


def whats_new(session):
    """Собирает информацию о новых статьях."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    response = get_response(session, whats_new_url)
    if response is None:
        logging.error('Тег не найден.')
        raise ParserFindTagException('Ничего не нашлось.')

    soup = BeautifulSoup(response.text, features=FUTURES)
    main_div = find_tag(
        soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(
        main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'})

    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, FUTURES)
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session):
    """Собирает информацию о последних версиях документации."""
    response = session.get(MAIN_DOC_URL)
    response.encoding = ENCODING
    soup = BeautifulSoup(response.text, features=FUTURES)
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        logging.error('Тег не найден.')
        raise ParserFindTagException('Ничего не нашлось.')
    results: list[str] = []
    pattern = PATTERN
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session):
    """Скачивает архив с документацией."""
    downloads_dir = BASE_DIR / 'downloads'
    try:
        downloads_dir.mkdir(exist_ok=True)
    except OSError as error:
        logging.error(f'Ошибка создания каталога: {downloads_dir}. '
                      f'Ошибка: {error}')
        raise ParserDirCreateException
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = session.get(downloads_url)
    response.encoding = ENCODING
    soup = BeautifulSoup(response.text, features=FUTURES)

    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(PDF_A4_TAG)})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    try:
        with open(archive_path, 'wb') as file:
            file.write(response.content)
        logging.info(f'Архив был загружен и сохранён: {archive_path}')
    except Exception as error:
        logging.exception(f'В процессе загрузки возникла ошибка: {error}')


def pep(session):
    """Собирает информацию о статусах PEP."""
    response = get_response(session, PEP_URL)
    soup = BeautifulSoup(response.text, features=FUTURES)

    logs: list[str] = []
    section = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    table = find_tag(section, 'table', attrs={'class': 'pep-zero-table'})
    tbody = find_tag(table, 'tbody')
    table_row = tbody.find_all('tr')
    count_pep = defaultdict(int)
    result = [('Статус', 'Количество')]
    for item in tqdm(table_row):
        table_data = find_tag(item, 'td')
        link = urljoin(PEP_URL, table_data.find_next_sibling().a['href'])
        response = get_response(session, link)
        soup = BeautifulSoup(response.text, features=FUTURES)
        status = table_data.text[1:]
        description_list = find_tag(soup, 'dl')
        status_page = (
            description_list.find(string='Status').
            parent.find_next_sibling().text
        )
        if status_page not in EXPECTED_STATUS[status]:
            logs.append(
                '\nНесовпадающие статусы:\n'
                f'{link}\n'
                f'Статус в карточке: {status_page}\n'
                f'Ожидаемые статусы: {EXPECTED_STATUS[status]}'
            )
        count_pep[status_page] += 1
    for status, count in count_pep.items():
        result.append((status, count))
    result.append(('Итого', len(table_row) - 1))
    return result


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()

        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.exception(
            f'Во время выполнения скрипта возникла ошибка {error}!')
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
