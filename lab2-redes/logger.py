import logging


class Logger():

    _logger = logging.getLogger()

    def __init__(self):
        formatter = logging.Formatter(
            "%(name)s - %(levelname)s - "
            "%(filename)s:%(funcName)s - %(message)s"
        )
        logging.StreamHandler().setFormatter(formatter)

    def log_error(self, msg: str):

        self._logger.error(msg, exc_info=True)

    def log_warning(self, msg: str):

        self._logger.warning(msg)

    def log_info(self, msg: str):

        self._logger.info(msg)

    def log_debug(self, msg: str):

        self._logger.debug(msg)
