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

    def __init__(self):
        """Init"""
        self._info_parsers = InfoParser.__subclasses__()  # noqa
        self._modbus_parsers = ModbusParser.__subclasses__()  # noqa
        self._parsers = Queue()

    def parse(self, data: FoxMessage):
        """Parse response"""

        if data.is_info():
            return self._parse_info(InfoMessage(data))

        if data.is_modbus():
            return self._parse_modbus(ModbusMessage(data))

        return None

    def _parse_info(self, data: InfoMessage):
        """Parse info message"""
        parsed_data = []
        for parser in self._info_parsers:
            parser = parser()
            if parser.can_parse(data):
                _LOGGER.info(f"Using info parser - {parser.__module__}")
                parsed_data.append(parser.parse_info(data))
        return parsed_data

    # TODO : add parsers as single list
    def _parse_modbus(self, data: ModbusMessage):
        """Parse info message"""
        if data.is_read_request():
            for parser in self._modbus_parsers:
                parser = parser()
                result, addresses = parser.can_parse(data)
                if result:
                    _LOGGER.info(f"Storing modbus parser - {parser.__module__}")
                    self._parsers.put((addresses, parser))
        elif data.is_read_response():
            parsed_data = []
            while not self._parsers.empty():
                addresses, parser = self._parsers.get_nowait()
                _LOGGER.info(f"Using modbus parser - {parser.__module__}")
                parsed_data.append(parser.parse_modbus(data, addresses))
            return parsed_data
