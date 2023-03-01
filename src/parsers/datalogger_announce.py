"""Inverter announce parser"""
from fox_message import FoxMessage
from parsers.info_parser import InfoParser

from .base_parser import BaseParser


class DataLoggerAnnounce(InfoParser, BaseParser):
    """Inverter announce parser"""

    _message_type = 0x2A
    _key = "dataloggerannounce"
    _message_start = 14
    _message_length = 15

    def can_parse(self, data: FoxMessage):
        """Can parse"""
        return data[0x02] == self._message_type

    def parse(self, data: FoxMessage):
        """Parse data"""
        return self._key, data.to_string(self._message_start, self._message_length)