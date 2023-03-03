"""Base connection"""
import logging

_LOGGER = logging.getLogger(__name__)


class Connection:
    """Manages connections"""

    def send(self, data):
        """Send data"""
        pass

    def receive(self):
        """Receieve data"""
        pass

    def initialise(self):
        """Initiate new connections"""
        pass
