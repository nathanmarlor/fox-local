"""Bidirectional communication"""
import logging
import queue
import threading
import time

from direct_connection import DirectConnection
from listen_connection import ListenConnection
from message_processor import MessageProcessor
from modbus_write import ModbusWrite

# from modbus_request import ModbusRequest

_LOGGER = logging.getLogger(__name__)


class FoxBidirectional:
    """Bidirectional class"""

    def __init__(self):
        """Init"""
        self._stop_event = threading.Event()

    def run(self):
        """Run the loop"""

        while True:
            self._stop_event.clear()

            inverter_conn = ListenConnection(self._stop_event, "0.0.0.0", 10001)
            inverter_conn.initialise()

            cloud_conn = DirectConnection(self._stop_event, "foxesscloud.com", 10001)
            cloud_conn.initialise()

            processor = MessageProcessor()

            inv_cloud = threading.Thread(
                target=self.passthrough, args=(processor, inverter_conn, cloud_conn)
            )

            cloud_inv = threading.Thread(
                target=self.passthrough, args=(processor, cloud_conn, inverter_conn)
            )

            # refresh = threading.Thread(
            #    target=self.refresh, args=(processor, inverter_conn)
            # )

            # TODO: add mqtt to inverter
            # mqtt_inv = threading.Thread(
            #    target=self.passthrough, args=(processor, mqtt_conn, inverter_conn)
            # )

            inv_cloud.start()
            cloud_inv.start()
            # refresh.start()
            inv_cloud.join()
            cloud_inv.join()
            # refresh.join()

            _LOGGER.info("Restarting bidirectional event loop after 5s")
            time.sleep(5)

    def refresh(self, processor, client):
        """Refresh thread"""
        time.sleep(45)
        while not self._stop_event.is_set():
            _LOGGER.debug("Sending refresh request")
            # request = ModbusRequest(41001, 6).build()
            request = ModbusWrite(41000, 1).build()
            processor.parse(request)
            client.send(request)
            time.sleep(10)

    def passthrough(self, processor, client, server):
        """Loop to receive from inverter and send to cloud"""

        while not self._stop_event.is_set():
            try:
                data = client.receive()
            except queue.Empty:
                continue
            results = processor.parse(data)
            if results:
                for result in results:
                    _LOGGER.debug(f"Sending result to MQTT - {result}")
                    # TODO: forward to MQTT
            server.send(data)
