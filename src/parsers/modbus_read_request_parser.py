"""Inverter announce parser"""
from fox_bytes import FoxBytes

from .base_parser import BaseParser


class ModbusReadRequestParser(BaseParser):
    """Inverter announce parser"""

    _message_type = 0x11
    _modbus_holding_read = 0x03
    _modbus_input_read = 0x04
    _key = "modbusinputread"

    def can_parse(self, data: FoxBytes):
        """Can parse"""
        return (
            self.is_modbus(data)
            and (data[0x02] == self._message_type)
            and (
                (data[0x0A] == self._modbus_holding_read)
                or (data[0x0A] == self._modbus_input_read)
            )
        )

    def parse(self, data: FoxBytes):
        """Parse data"""
        address = (data[0xB] << 8) | data[0xC]
        length = (data[0xD] << 8) | data[0xE]
        return self._key, (address, length)
