"""Process responses from the inverter"""
import logging
from queue import Queue

from fox_message import FoxMessage
from info_message import InfoMessage
from modbus_message import ModbusMessage
from parsers import *  # noqa

_LOGGER = logging.getLogger(__name__)


class MessageProcessor:
    """Process responses from the inverter"""

    _parsers = Queue()

    def parse(self, data: FoxMessage):
        """Parse response"""

        if data.is_info():
            _LOGGER.debug("Got info message")
            return self._parse_info(InfoMessage(data))

        if data.is_modbus():
            _LOGGER.debug("Got modbus message")
            return self._parse_modbus(ModbusMessage(data))

        return None

    def _parse_info(self, data: InfoMessage):
        """Parse info message"""
        for parser in InfoParser.__subclasses__():  # noqa
            parser = parser()
            if parser.can_parse(data):
                _LOGGER.info(f"Using info parser - {parser.__module__}")
                result = parser.parse(data)
                _LOGGER.info(f"Parsed - {result}")
                return result

    def _parse_modbus(self, data: ModbusMessage):
        """Parse info message"""
        if data.is_read_request():
            for parser in ModbusParser.__subclasses__():  # noqa
                # TODO: grab all parsers
                parser = parser()
                if parser.can_parse(data):
                    _LOGGER.info(f"Using modbus parser - {parser.__module__}")
                    self._parsers.put(parser)
        elif data.is_read_response():
            parser = self._parsers.get(False)
            return parser.parse(data)
