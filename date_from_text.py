import argparse
import logging
import sys
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from typing import Union
from logging_filters import FilterInfo, FilterError

MONTHS = {
    'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4,
    'ма': 5, 'июн': 6, 'июл': 7, 'авг': 8,
    'сен': 9, 'окт': 10, 'ноя': 11, 'дек': 12,
}
WEEKDAYS = {
    'понедельник': 0, 'вторник': 1, 'среда': 2, 'четверг': 3,
    'пятница': 4, 'суббота': 5, 'воскресенье': 6,
}


def get_date_from_text(text: str) -> Union[datetime, None]:
    """
    Function gives string request "day of week of month" and return date in current year.

    :param text: request in the format: "day of the week of the month", example: "1-е воскресенье ноября"
    :return: date of datetime type, in the formate: 2024-01-01 00:00:00 or None,
    if a value of the function argument is incorrect, example: "10-е воскресенье ноября"
    """
    logger = log_init()

    validate_data(text, logger)
    raw_number, weekday_, raw_month = text.split()
    sequence_number = int(raw_number.split('-')[0])
    weekday_ = WEEKDAYS.get(weekday_)
    month = int(*[MONTHS.get(month) for month in MONTHS.keys() if month in raw_month])
    year = datetime.now().year

    proxima_date = datetime(year=year, month=month, day=1)

    count = 0
    for i in range(7 * sequence_number):
        if proxima_date.weekday() == weekday_ and proxima_date.month == month:
            count += 1
            if count == sequence_number:
                target_date = proxima_date
                logger.info(f'{target_date = }')
                return target_date
        proxima_date += timedelta(days=1)
    logger.error(ValueError(f'{text} - not exist'))
    return None


def validate_data(text: str, logger: logging.Logger):
    """
     Function gives string request "day of week of month" and check it.
     If a value is incorrect, raise an error and logging it in a file.

    :param text: string request
    :return:
    """

    if not isinstance(text, str):
        logger.error(TypeError(f'Type of the specified variable must be string'))
        raise TypeError(f'Type of the specified variable must be string')
    if len(text.split()) != 3:
        logger.error(ValueError(f'Incorrect content of the specified variable. Text len != 3'))
        raise ValueError(f'Incorrect content of the specified variable. Format should be: “1-й четверг ноября”')
    if not text.split()[0][0].isdigit():
        logger.error(ValueError(f'Incorrect content of the specified variable. First char must be digit'))
        raise ValueError(f'Incorrect content of the specified variable. Format should be: “1-й четверг ноября”')


def cmdl_parser() -> str:
    """
    Function create object for parsing command line strings into Python objects.
    :return: Function parameter from command line
    """
    parser = argparse.ArgumentParser(description='Принимает запрос: день недели месяца. Возвращает дату.')
    parser.add_argument('-d', '--date', type=str, default='1-й понедельник января',
                        help='Day of week of month')
    args = parser.parse_args()
    return args.date


def log_init() -> logging.Logger:
    """
    Function create an instance of the Logger class and config it.
    :return: object - instance of the Logger class
    """
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)

    formatter = logging.Formatter(fmt="{name} - {asctime} - {levelname} - {message}", style="{")
    file_name = sys.argv[0].split('\\')[-1].split('.')[0]

    handler_info = logging.FileHandler(filename=f"{file_name}_info.log", mode='a', encoding='utf-8')
    handler_info.addFilter(FilterInfo())
    handler_info.setFormatter(formatter)
    logger.addHandler(handler_info)

    handler_error = RotatingFileHandler(filename=f"{file_name}_error.log", mode='a', encoding='utf-8',
                                        maxBytes=10000, backupCount=3)
    handler_error.addFilter(FilterError())
    handler_error.setFormatter(formatter)
    logger.addHandler(handler_error)
    return logger


if __name__ == "__main__":
    print(get_date_from_text(cmdl_parser()))
    #python date_from_text.py
    #python date_from_text.py -d '3-й понедельник мая'
