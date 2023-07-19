class ParserFindTagException(Exception):
    """
    Вызывается, когда парсер не может найти тег.
    """
    pass


class ParserFileOutputException(Exception):
    """
    Вызывается, когда парсер не
    может создать сохранить файл.
    """
    pass


class ParserDirCreateException(Exception):
    """
    Вызывается, когда парсер не
    может создать каталог.
    """
    pass
