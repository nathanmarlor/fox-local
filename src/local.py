"""Bidirectional communication"""
import logging
import threading

from listen_connection import ListenConnection
from message_processor import MessageProcessor

_LOGGER = logging.getLogger(__name__)


class FoxLocal:
    """Bidirectional class"""

    def run(self):
        """Run the loop"""
        inverter_conn = ListenConnection("0.0.0.0", 10001)
        inverter_conn.initialise()

        threading.Thread(target=self.local, args=(inverter_conn)).start()

    def local(self, client):
        """Loop to receive from inverter and send to MQTT"""
        processor = MessageProcessor()

        while True:
            data = client.receive()
            result = processor.parse(data)
            if result is not None:
                _LOGGER.debug(f"Sending result to MQTT - {result}")
                # TODO: forward to MQTT

                # if result has reply
                #    send to inverter (client.send)
