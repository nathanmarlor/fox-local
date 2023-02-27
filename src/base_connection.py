import logging
import queue
import threading

_LOGGER = logging.getLogger(__name__)


class BaseConnection:
    """Manages connections"""

    def __init__(self, host, port):
        """Init"""
        self._host = host
        self._port = port
        self._send_queue = queue.Queue()
        self._receive_queue = queue.Queue()

    def start(self, stop_event, sock):
        """Start threading loop"""
        send = threading.Thread(
            target=self._send_thread, args=(stop_event, sock, self._send_queue)
        )
        receive = threading.Thread(
            target=self._receive_thread, args=(stop_event, sock, self._receive_queue)
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
        return self._receive_queue.get(block=True)

    def _send_thread(self, stop_event, sock, send_queue):
        """Send thread"""
        while True:
            if stop_event.is_set():
                break
            try:
                data = send_queue.get(True, 1)
                sock.sendall(data)
                _LOGGER.debug(f"Sent to ({self._host}): {data}")
            except queue.Empty:
                continue
            except Exception as ex:
                _LOGGER.warning(f"({self._host}) Send exception: {ex}")
                stop_event.set()

    def _receive_thread(self, stop_event, sock, receive_queue):
        """Receieve thread"""
        while True:
            if stop_event.is_set():
                break
            try:
                data = sock.recv(1024)
                if not data:
                    raise ConnectionError(
                        f"({self._host}) - Connection closed by remote host"
                    )
                receive_queue.put(data)
                _LOGGER.debug(f"Received from ({self._host}): {data}")
            except Exception as ex:
                _LOGGER.warning(f"({self._host}) Receive exception: {ex}")
                stop_event.set()
