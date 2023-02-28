"""Inverter announce parser"""
from fox_bytes import FoxBytes

from .base_parser import BaseParser


class DataLoggerAnnounce(BaseParser):
    """Inverter announce parser"""

    _message_type = 0x2A
    _key = "dataloggerannounce"
    _message_start = 14
    _message_length = 15

    def can_parse(self, data: FoxBytes):
        """Can parse"""
        return self.is_info(data) and (data[0x02] == self._message_type)

    def parse(self, data: FoxBytes):
        """Parse data"""
        return self._key, data.to_string(self._message_start, self._message_length)
