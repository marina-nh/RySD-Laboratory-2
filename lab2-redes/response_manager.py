import errno
import socket
import constants

from logger import Logger
from command import Command
from hftp_exception import HFTPException

logger = Logger()


class ResponseManager():
    def __init__(self, socket: str):
        self.socket: socket.socket = socket

    def send_error(self, exception: HFTPException):
        logger.log_debug(f"Exception type: {type(exception)}")
        logger.log_error(f"error_code: {exception.error_code}")

        # El comando "get_file_listing" no retorna con \r\n
        # por lo que este comando genérico funciona para todos los casos
        self.send_response(exception.error_code, Command("dismiss", []), [])

    def send_response(self, code: int, command: Command, lines: list = []):
        logger.log_debug(
            f"Executing ResponseManager.send_response() with code {code}"
        )

        self.send_line(f"{code} {constants.code_messages[code]}")

        for line in lines:
            self.send_line(line)

        if(command.name == "get_file_listing"):
            self.send_line("")

    def send_line(self, line: str):
        logger.log_info(f"Socket ===> {line}\\r\\n")

        try:
            self.socket.send((line + constants.EOL).encode("ascii"))
        except (IOError, BrokenPipeError) as err:
            if err.errno == errno.EPIPE or isinstance(err, BrokenPipeError):
                logger.log_error(
                    f"Tried send_line('{line}') but socket is closed."
                )
