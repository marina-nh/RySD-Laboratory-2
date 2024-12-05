import constants

from logger import Logger

logger = Logger()


class HFTPException(Exception):

    def __init__(
            self,
            error_code: int,
            error_msg: str,
            error_name="HFTP Exception"):
        self.error_code = error_code
        self.error_msg = error_msg
        self.error_name = error_name
        logger.log_warning(f"HFTPException: {self}")

    def __str__(self):
        return f"[{self.error_code}] {self.error_name}: {self.error_msg}"


class MalformedParserException(HFTPException):

    def __init__(self):
        super().__init__(
            constants.BAD_EOL,
            "found \\n without \\r",
            constants.PARSER_STATUS_MALFORMED
        )


class UnknownParserException(HFTPException):

    def __init__(self):
        super().__init__(
            constants.BAD_REQUEST,
            "Request was no accepted",
            constants.UnknownParserException
        )


class InternalErrorException(HFTPException):

    def __init__(self, exception: str):
        super().__init__(
            constants.INTERNAL_ERROR,
            str(exception),
            constants.code_messages[constants.INTERNAL_ERROR]
        )


class FileNotFoundException(HFTPException):

    def __init__(self):
        super().__init__(
            constants.FILE_NOT_FOUND,
            "File not found on the Server permitted directory",
            constants.code_messages[constants.FILE_NOT_FOUND]
        )


class InvalidArgumentsException(HFTPException):

    def __init__(self):
        super().__init__(
            constants.INVALID_ARGUMENTS,
            "Invalid Arguments for current command",
            constants.code_messages[constants.INVALID_ARGUMENTS]
        )


class InvalidCommandException(HFTPException):

    def __init__(self):
        super().__init__(
            constants.INVALID_COMMAND,
            "Invalid Command",
            constants.code_messages[constants.INVALID_COMMAND]
        )


class BadOffsetException(HFTPException):

    def __init__(self):
        super().__init__(
            constants.BAD_OFFSET,
            "Amount of bytes out of bounds",
            constants.code_messages[constants.BAD_OFFSET]
        )
