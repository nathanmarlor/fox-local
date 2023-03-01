"""Inverter charge period parser"""
from modbus_message import ModbusMessage
from parsers.modbus_parser import ModbusParser

from .base_parser import BaseParser


class ChargePeriod(ModbusParser, BaseParser):
    """Inverter charge period parser"""

    _key = "chargeperiod"
    _address = 41001

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return self._address in data.get_all_addresses()

    def parse(self, data: ModbusMessage):
        """Parse data"""
        # TODO: parse out charge period bytes
        return "chargeperiod"
