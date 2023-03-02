"""Inverter serial number parser"""
from fox_message import FoxMessage

from ..base_parser import BaseParser
from .info_parser import InfoParser


class InverterAnnounce(InfoParser, BaseParser):
    """Inverter serial number parser"""

    _message_type = 0x06
    _key = "inverterannounce"

    def can_parse(self, data: FoxMessage):
        """Can parse"""
        return data[0x02] == self._message_type

    def parse_info(self, data: FoxMessage):
        """Parse data"""
        return self._key, data.to_string(15, 15)
