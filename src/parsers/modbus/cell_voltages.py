"""Inverter cell voltages parser"""
from modbus_message import ModbusMessage

from ..base_parser import BaseParser
from .modbus_parser import ModbusParser


class CellVoltages(ModbusParser, BaseParser):
    """Inverter cell voltages  parser"""

    _key = "cellvoltages1-50"
    _address = 60000
    _length = 50

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return data.address_is_present(self._address, self._length)

    def parse_modbus(self, data: ModbusMessage, index):
        """Parse data"""
        parsed = data.get_data()[index : index + self._length]
        dictionary = {}

        for i, value in enumerate(parsed):
            key = f"cell_{i+1}"
            dictionary[key] = value

        return self._key, dictionary
