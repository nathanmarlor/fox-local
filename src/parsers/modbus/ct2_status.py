"""Inverter CT2 parser"""
from modbus_message import ModbusMessage

from ..base_parser import BaseParser
from .modbus_parser import ModbusParser


class CT2Status(ModbusParser, BaseParser):
    """Inverter CT2 parser"""

    _key = "ct2status"
    _address = 40011
    _length = 1

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return data.address_is_present(self._address, self._length)

    def parse_modbus(self, data: ModbusMessage, index):
        """Parse data"""
        parsed = data.get_data()[index : index + self._length]
        return self._key, {"ct2_status": parsed[0]}
