"""MQTT Connection"""
import logging
import queue
import threading

import paho.mqtt.client as mqtt
from connection import Connection

_LOGGER = logging.getLogger(__name__)


class MQTTConnection(Connection):
    """MQTT Connection"""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None
        self.queue = queue.Queue()

    def send(self, data):
        """Send data"""
        pass

    def receive(self):
        """Receieve data"""
        return self.queue.get(True, 1)

    def _on_connect(self, client, userdata, flags, rc):
        _LOGGER.info(f"MQTT connected to {self.host}")
        client.subscribe("/fox/h1/raw_read")

    def _on_message(self, client, userdata, msg):
        _LOGGER.debug(f"Inbound MQTT message {msg.payload}")
        self.queue.put(str(msg.payload.decode("utf-8")))

    def initialise(self):
        """Initiate new connections"""
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        threading.Thread(target=self._start).start()

    def _start(self):
        self.client.connect(self.host, self.port, 60)
        self.client.loop_forever()
