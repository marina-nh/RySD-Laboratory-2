#!/usr/bin/env python

import sys
import socket
import signal
import logging
import _thread
import optparse
import constants

from time import sleep
from logger import Logger
from connection import Connection


logger = Logger()


class Server(object):
    MAX_AMOUNT_CLIENTS = 5

    def __init__(
        self,
        addr=constants.DEFAULT_ADDR,
        port=constants.DEFAULT_PORT,
        directory=constants.DEFAULT_DIR
    ):
        print("Serving %s on %s:%s." % (directory, addr, port))

        self.directory = directory

        # Creación del socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Configuración
        self.socket.bind((addr, port))

        # Listening
        self.socket.listen(self.MAX_AMOUNT_CLIENTS)

    def handle_client_listen(self, lock: _thread.LockType):
        lock.acquire()

        try:
            while True:
                # Aceptar una conexión al server, crear una
                # connection para la conexión y atenderla hasta que termine.
                connection = Connection(
                    self.socket.accept()[0], self.directory
                )
                connection.handle()
        except KeyboardInterrupt:
            lock.release()
            raise KeyboardInterrupt

    def serve(self):
        self.threads = []
        self.locks = []
        for i in range(self.MAX_AMOUNT_CLIENTS):
            logger.log_debug(f"Starting Connection listener for client {i}")
            lock = _thread.allocate_lock()
            self.locks.append(lock)

            current_thread_id = _thread.start_new_thread(
                self.handle_client_listen,
                (lock,)
            )
            self.threads.append(current_thread_id)
            logger.log_debug(
                f">> Thread_id {current_thread_id} for client {i} started"
            )

        sleep(1)
        self.get_all_locks()

    def get_all_locks(self):
        for lock in self.locks:
            lock.acquire()

    def close(self):
        logger.log_warning("Cerrando el servidor...")
        self.socket.close()


def main():
    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar",
        default=constants.DEFAULT_PORT
    )

    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar",
        default=constants.DEFAULT_ADDR
    )

    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido",
        default=constants.DEFAULT_DIR
    )

    parser.add_option(
        "-v", "--verbose",
        dest="level",
        action="store",
        help="Determina cuanta información de depuración mostrar"
        "(valores posibles son: ERROR, WARN, INFO, DEBUG)",
        default="ERROR"
    )

    options, args = parser.parse_args()
    setup_logger(options.level)

    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    try:
        server = Server(options.address, port, options.datadir)

        def handle_sigterm(signalNumber, frame):
            logger.log_warning(f"Received SIGTERM. Closing Sockets")
            server.close()
            sys.exit()

        signal.signal(signal.SIGTERM, handle_sigterm)

        server.serve()
    except KeyboardInterrupt as keyboardInterrupt:
        server.close()
        raise keyboardInterrupt


def setup_logger(level):
    DEBUG_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN': logging.WARNING,
        'ERROR': logging.ERROR,
    }

    # Setar verbosidad
    code_level = DEBUG_LEVELS.get(level)  # convertir el str en codigo
    logging.basicConfig(format='[%(levelname)s] - %(message)s')
    logger = Logger()
    logger._logger.setLevel(code_level)


if __name__ == '__main__':
    main()
