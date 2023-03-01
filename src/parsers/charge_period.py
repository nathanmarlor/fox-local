"""Inverter charge period parser"""
from datetime import time

from modbus_message import ModbusMessage
from parsers.modbus_parser import ModbusParser

from .base_parser import BaseParser


class ChargePeriod(ModbusParser, BaseParser):
    """Inverter charge period parser"""

    _key = "chargeperiod"
    _address = 41001
    _length = 6

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return data.address_is_present(self._address, self._length)

    def parse(self, data: ModbusMessage):
        """Parse data"""
        parsed = data.get_data()
        return {
            "period1_enabled": bool(parsed[0]),
            "period1_start": self._get_time(parsed[1]),
            "period1_end": self._get_time(parsed[2]),
            "period2_enabled": bool(parsed[3]),
            "period2_start": self._get_time(parsed[4]),
            "period2_end": self._get_time(parsed[5]),
        }

    def _get_time(self, raw_time):
        """Get time from an integer"""
        hours = raw_time // 256
        minutes = raw_time - (hours * 256)
        return time(hour=hours, minute=minutes)
