"""Inverter cell voltages parser"""
from modbus_message import ModbusMessage
from parsers.modbus_parser import ModbusParser

from .base_parser import BaseParser


class CellVoltages(ModbusParser, BaseParser):
    """Inverter cell voltages  parser"""

    _key = "cellvoltages1-50"
    _address = 60000
    _length = 50

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return data.address_is_present(self._address, self._length)

    def parse(self, data: ModbusMessage):
        """Parse data"""
        parsed = data.get_data()
        dictionary = {}

        for i, value in enumerate(parsed):
            key = f"cell_{i+1}"
            dictionary[key] = value

        return dictionary
