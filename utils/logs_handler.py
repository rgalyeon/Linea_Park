import os


def filter_out_utils(record):
    # Путь к папке 'utils' относительно корня проекта или места запуска скрипта
    utils_path = os.path.abspath('utils')

    # Путь к файлу, из которого было сделано лог-сообщение
    log_path = os.path.abspath(record["file"].path)

    # Фильтрация логов, исключая файлы внутри папки 'utils'
    return not log_path.startswith(utils_path)
