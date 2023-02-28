"""Inverter serial number parser"""
from fox_message import FoxMessage
from parsers.info_parser import InfoParser

from .base_parser import BaseParser


class InverterAnnounce(InfoParser, BaseParser):
    """Inverter serial number parser"""

    _message_type = 0x06
    _key = "inverterannounce"

    def can_parse(self, data: FoxMessage):
        """Can parse"""
        return data[0x02] == self._message_type

    def parse(self, data: FoxMessage):
        """Parse data"""
        return self._key, data.to_string(15, 15)
