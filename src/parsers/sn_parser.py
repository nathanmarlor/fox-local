"""Inverter serial number parser"""
from fox_bytes import FoxBytes

from .base_parser import BaseParser


class SnParser(BaseParser):
    """Inverter serial number parser"""

    _message_type = 0x06
    _key = "sn"

    def can_parse(self, data: FoxBytes):
        """Can parse"""
        return self.is_info(data) and (data[0x02] == self._message_type)

    def parse(self, data: FoxBytes):
        """Parse data"""
        return self._key, data.to_string(9, 15)
