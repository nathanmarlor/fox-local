import threading
import logging
from listen_connection import ListenConnection
from direct_connection import DirectConnection

_LOGGER = logging.getLogger(__name__)


class FoxBidirectional:
    """Bidirectional class"""

    def run(self):
        """Run the loop"""
        inverter_conn = ListenConnection("0.0.0.0", 10001)
        inverter_conn.initialise()

        cloud_conn = DirectConnection("foxesscloud.com", 10001)
        cloud_conn.initialise()

        threading.Thread(
            target=self.passthrough, args=(inverter_conn, cloud_conn)
        ).start()

        threading.Thread(
            target=self.passthrough, args=(cloud_conn, inverter_conn)
        ).start()

    def passthrough(self, client, server):
        """Loop to receive from inverter and send to cloud"""
        while True:
            data = client.receive()
            server.send(data)
