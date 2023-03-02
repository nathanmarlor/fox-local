"""Inverter raw modbus parser"""
from modbus_message import ModbusMessage

from ..base_parser import BaseParser
from .modbus_parser import ModbusParser


class ModbusRaw(ModbusParser, BaseParser):
    """Inverter raw modbus parser"""

    _key = "modbus-raw"

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return True, 0

    def parse_modbus(self, data: ModbusMessage, index):
        """Parse data"""
        parsed = data.get_data()

        return self._key, (data.get_all_addresses(), parsed)
