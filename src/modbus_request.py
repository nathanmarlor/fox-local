"""Modbus request message"""
from modbus_builder import ModbusBuilder


class ModbusRequest(ModbusBuilder):
    """Modbus request message"""

    _function = 0x3
    _type_byte = 0x11

    def __init__(
        self,
        address,
        quantity,
    ):
        self._address = address
        self._quantity = quantity

    def build(self):
        """Modbus request"""
        data = [
            1,
            self._function,
            (self._address >> 8) & 0xFF,
            self._address & 0xFF,
            (self._quantity >> 8) & 0xFF,
            self._quantity & 0xFF,
        ]
        return self._to_bytes(self._type_byte, data)
