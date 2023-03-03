"""Modbus request message"""
from modbus_builder import ModbusBuilder


class ModbusWrite(ModbusBuilder):
    """Modbus request message"""

    _function = 0x06
    _type_byte = 0x12
    _quantity = 1

    def __init__(self, address, data):
        self._address = address
        self._data = data

    def build(self):
        """Modbus request"""
        data = [
            1,
            self._function,
            (self._address >> 8) & 0xFF,
            self._address & 0xFF,
            (self._quantity >> 8) & 0xFF,
            self._quantity & 0xFF,
            self._data,
        ]
        return self._to_bytes(self._type_byte, data)
