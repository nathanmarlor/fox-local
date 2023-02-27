import socket
import threading
import time
import logging
from base_connection import BaseConnection

_LOGGER = logging.getLogger(__name__)


class ListenConnection(BaseConnection):
    """Manages connections"""

    def initialise(self):
        """Initiate new connections"""
        threading.Thread(target=self._initialise).start()

    def _initialise(self):
        """Internal loop to maintain connection"""
        while True:
            stop_event = threading.Event()
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
                    server_sock.bind((self._host, self._port))
                    server_sock.listen()
                    _LOGGER.info(f"Listening on {self._host}:{self._port}")

                    client_sock, addr = server_sock.accept()
                    _LOGGER.info(f"Connected to {addr}")

                    with client_sock:
                        self.start(stop_event, client_sock)
            except socket.error as ex:
                _LOGGER.warning(f"Listener ({self._host}) socket exception: {ex}")
                time.sleep(5)
                continue
