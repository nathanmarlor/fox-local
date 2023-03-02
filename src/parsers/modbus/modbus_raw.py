"""Inverter raw modbus parser"""
from modbus_message import ModbusMessage

from ..base_parser import BaseParser
from .modbus_parser import ModbusParser


class ModbusRaw(ModbusParser, BaseParser):
    """Inverter raw modbus parser"""

    _key = "modbus-raw"

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return True

    def parse_modbus(self, data: ModbusMessage, addresses):
        """Parse data"""
        parsed = data.get_data()

        return self._key, (addresses, parsed)
