"""Listen connection"""
import logging
import select
import socket
import threading

from socket_connection import SocketConnection

_LOGGER = logging.getLogger(__name__)


class ListenConnection(SocketConnection):
    """Manages connections"""

    def initialise(self):
        """Initiate new connections"""
        threading.Thread(target=self._initialise).start()

    def _initialise(self):
        """Internal loop to maintain connection"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            try:
                server_sock.bind((self._host, self._port))
                server_sock.listen(1)
                _LOGGER.info(f"Listening on {self._host}:{self._port}")
                while not self._stop_event.is_set():
                    read, _, _ = select.select([server_sock], [], [], 1)
                    if server_sock in read:
                        try:
                            client_socket, addr = server_sock.accept()
                            _LOGGER.info(f"Connected to {addr}")
                            with client_socket:
                                self.start(client_socket)
                        except socket.error as ex:
                            _LOGGER.warning(f"Error accepting connection: {ex}")
            except socket.error as ex:
                _LOGGER.warning(f"Listener ({self._host}) socket exception: {ex}")
                self._stop_event.set()
