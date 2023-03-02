"""Base connection"""
import logging
import queue
import select
import threading

from fox_message import FoxMessage

_LOGGER = logging.getLogger(__name__)


class BaseConnection:
    """Manages connections"""

    def __init__(self, stop_event, host, port):
        """Init"""
        self._stop_event = stop_event
        self._host = host
        self._port = port
        self._send_queue = queue.Queue()
        self._receive_queue = queue.Queue()

    def start(self, sock):
        """Start threading"""
        send = threading.Thread(target=self._send_thread, args=(sock, self._send_queue))
        receive = threading.Thread(
            target=self._receive_thread,
            args=(sock, self._receive_queue),
        )

        send.start()
        receive.start()
        send.join()
        receive.join()

    def send(self, data):
        """Send data"""
        self._send_queue.put(data)

    def receive(self):
        """Receieve data"""
        return self._receive_queue.get(True, 1)

    def _send_thread(self, sock, send_queue):
        """Send thread"""
        while not self._stop_event.is_set():
            try:
                data = send_queue.get(True, 1)
                sock.sendall(bytes(data))
            except queue.Empty:
                continue
            except Exception as ex:
                _LOGGER.warning(f"({self._host}) Send exception: {ex}")
                self._stop_event.set()

    def _receive_thread(self, sock, receive_queue):
        """Receieve thread"""
        while not self._stop_event.is_set():
            try:
                read, _, _ = select.select([sock], [], [], 1)
                if sock in read:
                    data = FoxMessage(sock.recv(1024))
                    data = FoxMessage(
                        b"\x7f\x7f\x11\xcex\xfc4\x00\x06\x01\x03\xa7\xf8\x00\x1b7\xaf\xf7\xf7"
                    )
                    if not data:
                        raise ConnectionError(
                            f"({self._host}) - Connection closed by remote host"
                        )
                    receive_queue.put(data)
            except Exception as ex:
                _LOGGER.warning(f"({self._host}) Receive exception: {ex}")
                self._stop_event.set()
