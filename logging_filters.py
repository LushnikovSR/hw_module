import logging


class FilterInfo(logging.Filter):
    NUMERIC_VALUE_INFO_LEVEL = 20

    def filter(self, record: logging.LogRecord) -> int:
        if record.levelno == self.NUMERIC_VALUE_INFO_LEVEL:
            return record.levelno


class FilterError(logging.Filter):
    NUMERIC_VALUE_ERROR_LEVEL = 40

    def filter(self, record: logging.LogRecord) -> int:
        if record.levelno == self.NUMERIC_VALUE_ERROR_LEVEL:
            return record.levelno
