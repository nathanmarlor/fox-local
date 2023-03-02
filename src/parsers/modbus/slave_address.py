"""Inverter slave address parser"""
from modbus_message import ModbusMessage

from ..base_parser import BaseParser
from .modbus_parser import ModbusParser


class SlaveAddress(ModbusParser, BaseParser):
    """Inverter slave address parser"""

    _key = "slaveaddress"
    _address = 40012
    _length = 1

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return data.address_is_present(self._address, self._length)

    def parse_modbus(self, data: ModbusMessage, addresses):
        """Parse data"""
        index = addresses.index(self._address)
        parsed = data.get_data()[index : index + self._length]
        return self._key, {"slave_address": parsed[0]}
