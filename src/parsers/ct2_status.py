"""Inverter CT2 parser"""
from modbus_message import ModbusMessage
from parsers.modbus_parser import ModbusParser

from .base_parser import BaseParser


class CT2Status(ModbusParser, BaseParser):
    """Inverter CT2 parser"""

    _key = "ct2status"
    _address = 41011
    _length = 1

    def can_parse(self, data: ModbusMessage):
        """Can parse"""
        return data.address_is_present(self._address, self._length)

    def parse(self, data: ModbusMessage, index):
        """Parse data"""
        parsed = data.get_data()[index : index + self._length]
        return {"ct2_status": parsed[0]}
