import socket
import threading
import time
from base_connection import BaseConnection


class DirectConnection(BaseConnection):
    """Manages connections"""

    def initialise(self):
        """Initiate new connections"""
        threading.Thread(target=self._initialise).start()

    def _initialise(self):
        """Internal loop to maintain connection"""
        while True:
            stop_event = threading.Event()
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
                    client_sock.connect((self._host, self._port))
                    print(f"Connected to {self._host}:{self._port}")

                    self.start(stop_event, client_sock)
            except socket.error as ex:
                print(f"Connect ({self._host}) socket exception: {ex}")
                time.sleep(5)
                continue
