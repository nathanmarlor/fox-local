"""Process responses from the inverter"""
import logging

from fox_bytes import FoxBytes
from parsers import *  # noqa

_LOGGER = logging.getLogger(__name__)


class MessageProcessor:
    """Process responses from the inverter"""

    def parse_response(self, data: FoxBytes):
        """Parse response"""
        for parser in BaseParser.__subclasses__():  # noqa
            parser = parser()
            if parser.can_parse(data):
                _LOGGER.info(f"Using parser - {parser.__module__}")
                result = parser.parse(data)
                _LOGGER.info(f"Got result - {result}")
