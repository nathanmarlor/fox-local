"""Bidirectional communication"""
import logging
import queue
import threading
import time

from listen_connection import ListenConnection

# from message_processor import MessageProcessor

_LOGGER = logging.getLogger(__name__)


class FoxLocal:
    """Bidirectional class"""

    _stop_event = threading.Event()

    def run(self):
        """Run the loop"""

        while True:
            self._stop_event.clear()

            inverter_conn = ListenConnection(self._stop_event, "0.0.0.0", 10001)
            inverter_conn.initialise()

            # mqtt_conn = MQTTConnection...

            # processor = MessageProcessor()

            # TODO: add inverter to mqtt
            # mqtt_inv = threading.Thread(
            #    target=self.passthrough, args=(processor, inverter_conn, mqtt_conn)
            # )

            # TODO: add mqtt to inverter
            # mqtt_inv = threading.Thread(
            #    target=self.passthrough, args=(processor, mqtt_conn, inverter_conn)
            # )

            _LOGGER.info("Restarting bidirectional event loop after 5s")
            time.sleep(5)

    def passthrough(self, processor, client, server):
        """Loop to receive from inverter and send to cloud"""

        while self._stop_event.is_set():
            try:
                data = client.receive()
            except queue.Empty:
                continue
            result, reply = processor.parse(data)
            # if reply is not None
            #    client.send(reply)
            if result is not None:
                _LOGGER.debug(f"Sending result to MQTT - {result}")
                server.send(data)
