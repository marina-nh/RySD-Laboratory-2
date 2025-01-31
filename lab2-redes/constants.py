DEFAULT_DIR = 'testdata'
DEFAULT_ADDR = '0.0.0.0'  # 0.0.0.0 representa todas las IPv4 del server
DEFAULT_PORT = 19500


EOL = '\r\n'


CODE_OK = 0
BAD_EOL = 100
BAD_REQUEST = 101
INTERNAL_ERROR = 199
"""
500
"""
INVALID_COMMAND = 200
INVALID_ARGUMENTS = 201
FILE_NOT_FOUND = 202
BAD_OFFSET = 203


HANDLER_STATUS_EXIT = "QUIT"
HANDLER_STATUS_OK = "OK"
HANDLER_INVALID_COMMAND = "INVALID_COMMAND"
HANDLER_INVALID_ARGUMENTS = "INVALID_ARGUMENTS"

PARSER_STATUS_OK = "OK"
PARSER_STATUS_MALFORMED = "MALFORMED"
PARSER_STATUS_UNKNOWN = "UNKNOWN"


code_messages = {
    CODE_OK: "OK",
    # 1xx: Errores fatales (no se pueden atender más pedidos)
    BAD_EOL: "BAD EOL",
    BAD_REQUEST: "BAD REQUEST",
    INTERNAL_ERROR: "INTERNAL SERVER ERROR",
    # 2xx: Errores no fatales (no se pudo atender este pedido)
    INVALID_COMMAND: "NO SUCH COMMAND",
    INVALID_ARGUMENTS: "INVALID ARGUMENTS FOR COMMAND",
    FILE_NOT_FOUND: "FILE NOT FOUND",
    BAD_OFFSET: "OFFSET EXCEEDS FILE SIZE",
}


def valid_status(s):
    return s in list(code_messages.keys())


def fatal_status(s):
    assert valid_status(s)
    return 100 <= s < 200


VALID_CHARS = set(".-_")
for i in range(ord('A'), ord('Z') + 1):
    VALID_CHARS.add(chr(i))
for i in range(ord('a'), ord('z') + 1):
    VALID_CHARS.add(chr(i))
for i in range(ord('0'), ord('9') + 1):
    VALID_CHARS.add(chr(i))
