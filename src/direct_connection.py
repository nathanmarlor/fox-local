"""Direct connection"""
import logging
import socket
import threading

from base_connection import BaseConnection

_LOGGER = logging.getLogger(__name__)


class DirectConnection(BaseConnection):
    """Manages connections"""

    def initialise(self):
        """Initiate new connections"""
        threading.Thread(target=self._initialise).start()

    def _initialise(self):
        """Internal loop to maintain connection"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
            try:
                _LOGGER.info(f"Attempting connection to {self._host}:{self._port}")
                client_sock.settimeout(10)
                client_sock.connect((self._host, self._port))
                _LOGGER.info(f"Connected to {self._host}:{self._port}")
                self.start(client_sock)
            except (socket.timeout, ConnectionRefusedError, OSError) as ex:
                _LOGGER.warning(f"Connect ({self._host}) socket exception: {ex}")
                self._stop_event.set()
