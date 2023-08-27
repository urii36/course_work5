import configparser

import os

path_os = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(path_os, 'database.ini')

def config(filename=file_name, section="postgresql"):
    # создаем парсер
    parser = configparser.ConfigParser()
    # прочитать конфигурационный файл
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Раздел {0} не найден в {1} файл".format(section, filename))
    return db

EMPLOYER_MAP = {
    "РутКод": 8642172,
    "AVC": 1626408,
    "МЕТИНВЕСТ": 2596438,
    "ФИНТЕХ": 2324020,
    "ОКБ": 2129243,
    "РусЭкспресс": 1875694,
    "IPChain": 3151408,
    "Wanted": 5174849,
    "AERODISK": 2723603,
    "Латера": 1050345,
    "Qualitica": 4181561,
}


