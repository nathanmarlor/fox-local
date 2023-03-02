"""Inverter raw info parser"""
from fox_message import FoxMessage

from ..base_parser import BaseParser
from .info_parser import InfoParser


class InfoRaw(InfoParser, BaseParser):
    """Inverter raw info parser"""

    _key = "info-raw"

    def can_parse(self, data: FoxMessage):
        """Can parse"""
        return True

    def parse_info(self, data: FoxMessage):
        """Parse data"""
        return self._key, (data[0x02], data)
