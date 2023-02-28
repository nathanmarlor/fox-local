"""Inverter workmode parser"""
from modbus_message import ModbusMessage
from parsers.modbus_parser import ModbusParser

from .base_parser import BaseParser


class WorkMode(ModbusParser, BaseParser):
    """Inverter workmode parser"""

    _key = "workmode"

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return True  # and work mode address

    def parse(self, data: ModbusMessage):
        """Parse data"""
        # parse out work mode bytes
        return "test"
