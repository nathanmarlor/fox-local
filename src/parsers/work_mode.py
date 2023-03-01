"""Inverter workmode parser"""
from modbus_message import ModbusMessage
from parsers.modbus_parser import ModbusParser

from .base_parser import BaseParser


class WorkMode(ModbusParser, BaseParser):
    """Inverter workmode parser"""

    _key = "workmode"
    _address = 41000

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return self._address in data.get_all_addresses()

    def parse(self, data: ModbusMessage):
        """Parse data"""
        # TODO: parse out work mode bytes
        return "workmode"
