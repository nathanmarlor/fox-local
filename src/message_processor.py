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
        parsers = [
            parser() for parser in self._info_parsers if parser().can_parse(data)
        ]
        _LOGGER.info(f"Using info parsers - ({self._parser_names(parsers)})")

        return [parser.parse_info(data) for parser in parsers]

    def _parse_modbus(self, data: ModbusMessage):
        """Parse info message"""
        if data.is_read_request():
            parsers = [
                parser() for parser in self._modbus_parsers if parser().can_parse(data)
            ]
            seq = data.get_sequence()
            _LOGGER.info(
                f"Storing modbus parsers ({seq}) - ({data.get_start_address()}:{data.get_length()}) ({self._parser_names(parsers)})"
            )
            self._parsers[seq] = (data.get_all_addresses(), parsers)
        elif data.is_read_response():
            seq = data.get_sequence()
            if seq in self._parsers:
                addresses, parsers = self._parsers.pop(seq)
                _LOGGER.info(
                    f"Using modbus parsers ({seq}) - ({self._parser_names(parsers)})"
                )
                return [parser.parse_modbus(data, addresses) for parser in parsers]

    def _parser_names(self, parsers):
        """Get parser names in a list"""
        return [parser.__module__ for parser in parsers]
