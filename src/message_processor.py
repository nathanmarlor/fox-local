"""Process responses from the inverter"""
import logging

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
        self._parsers = dict()

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

    def _parse_modbus(self, data: ModbusMessage):
        """Parse info message"""
        if data.is_read_request():
            parsers = [
                parser() for parser in self._modbus_parsers if parser().can_parse(data)
            ]
            seq = data.get_sequence()
            for parser in parsers:
                _LOGGER.info(f"Storing modbus parsers ({seq}) - {parser.__module__}")
            self._parsers[seq] = (data.get_all_addresses(), parsers)
        elif data.is_read_response():
            seq = data.get_sequence()
            if seq in self._parsers:
                addresses, parsers = self._parsers.pop(seq)
                for parser in parsers:
                    _LOGGER.info(f"Using modbus parser ({seq}) - {parser.__module__}")
                return [parser.parse_modbus(data, addresses) for parser in parsers]
