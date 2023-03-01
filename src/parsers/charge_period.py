"""Inverter charge period parser"""
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
        # TODO: parse out charge period bytes
        return "chargeperiod"
