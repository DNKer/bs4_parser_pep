# Парсер документации PEP

## Описание.

Парсер, который поможет быть в курсе важных изменений между основными версиями Python. Он соберает ссылки на статьи о нововведениях и достаёт из них справочную информацию: имя автора или редактора статьи, дата публикации и версия Python. Результат работы выводится в консоль построчно, в консоль в виде таблицы, а еще существует возможность сохранять (выгружать) результат в csv файл. Также при помощи приложения возможно скачать на локальный диск архив с документацией &#10069;

<img src="tests\fixture_data\Image.png" alt="drawing" width="800"/>

## Технологии .
[![Python](https://img.shields.io/badge/-Python-464646?style=plastic&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/) [![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=plastic&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
![Python](https://img.shields.io/badge/python-bs4-blue) ![Python](https://img.shields.io/badge/python-tqdm-blue)

![workflow](https://github.com/DNKer/bs4_parser_pep/actions/workflows/bs4_parser_pep_workflow/badge.svg?branch=master&event=push)

## Установка

> приводятся команды для `Windows`.

Клонировать репозитарий:

```bash
git clone git@github.com:DNKer/bs4_parser_pep.git
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/scripts/activate
```

Обновить систему управления пакетами:

```bash
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Перейти в папку "src":

```bash
cd src/
```

Запустить парсер в одном из режимов:

```bash
python main.py <parser_mode> <args>
```

## Аргументы парсера

Поддерживаются сокращенная и полная формы записи одного и того же аргумента: короткая, с одним символом - и длинная, с двумя символами -- (для примера: ```-h``` и ```--help```). Аргументы в длинной форме проще запомнить, а в короткой удобнее использовать.

+ **Вывести информацию о парсере:**
```bash
python main.py <parser_mode> -h
```
```bash
python main.py <parser_mode> --help
```

+ **Очистить кеш:**
```bash
python main.py <parser_mode> -c
```
```bash
python main.py <parser_mode> --clear-cache
```

+ Настроить режим отображения результатов:

Сохранение результатов в CSV файл:
```bash
python main.py <parser_mode> --o file
```
```bash
python main.py <parser_mode> --output file
```
Отображение результатов в табличном формате в консоли:
```bash
python main.py <parser_mode> --o pretty
```
```bash
python main.py <parser_mode> --output pretty
```

Если не указывать аргумент ```--output```, результат парсинга будет выведен в консоль (кроме режима ```download```):
```bash
python main.py <parser_mode>
```

#### Лицензия
###### Free Software, as Is 
###### _License Free_
###### Author: [Dmitry](https://github.com/DNKer), [Yandex practikum](https://practicum.yandex.ru)
###### 2023