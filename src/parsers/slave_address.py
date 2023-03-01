"""Inverter slave address parser"""
from modbus_message import ModbusMessage
from parsers.modbus_parser import ModbusParser

from .base_parser import BaseParser


class SlaveAddress(ModbusParser, BaseParser):
    """Inverter slave address parser"""

    _key = "slaveaddress"
    _address = 40012
    _length = 1

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return data.address_is_present(self._address, self._length)

    def parse(self, data: ModbusMessage, index):
        """Parse data"""
        parsed = data.get_data()[index : index + self._length]
        return {"slave_address": parsed[0]}
